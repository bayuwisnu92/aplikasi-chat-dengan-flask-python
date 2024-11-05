from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.controllers.auth_controller import index_register, index_login, index_logout
from app.models import User, ChatRoom, Chat
from app import db, socketio  # Import socketio
from flask_socketio import emit, join_room, leave_room

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def chatrooms():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user_id = session.get('user_id')
    username = session.get('username')
    users = User.query.filter(User.id != user_id).all()
    return render_template('chatroom/chatrooms.html', users=users, username=username)

@main.route('/chat/<int:room_id>', methods=['GET', 'POST'])
def personal_chat(room_id):
    user_id = session.get('user_id')
    chatroom = ChatRoom.query.get_or_404(room_id)

    if user_id not in [chatroom.user1_id, chatroom.user2_id]:
        flash('You do not have permission to access this chatroom.', 'danger')
        return redirect(url_for('main.chatrooms'))

    messages = Chat.query.filter_by(room_id=room_id).order_by(Chat.timestamp).all()

    return render_template('chatroom/personal_chat.html', chatroom=chatroom, messages=messages)

@socketio.on('send_message')
def handle_send_message(data):
    user_id = session.get('user_id')
    room_id = data['room_id']
    message_content = data['message']

    # Save the message to the database
    new_message = Chat(user_id=user_id, room_id=room_id, message=message_content)
    db.session.add(new_message)
    db.session.commit()

    # Broadcast the message to the room
    emit('receive_message', {
        'user_id': user_id,
        'username': session.get('username'),
        'message': message_content,
        'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }, room=room_id)

@socketio.on('join')
def on_join(data):
    room = data['room_id']
    join_room(room)
    emit('status', {'msg': f"{session.get('username')} has joined the room."}, room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room_id']
    leave_room(room)
    emit('status', {'msg': f"{session.get('username')} has left the room."}, room=room)

# Route lainnya...

@main.route('/login', methods=['GET', 'POST'])
def login():
    return index_login()

@main.route('/register', methods=['GET', 'POST'])
def register():
    return index_register()

@main.route('/logout')
def logout():
    return index_logout()

def login_required(func):
    """ Custom decorator to check if user is logged in via session. """
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@main.route('/create_private_chat/<username>', methods=['GET', 'POST'])
def create_private_chat(username):
    current_user_id = session.get('user_id')
    current_user_obj = User.query.get(current_user_id)
    target_user = User.query.filter_by(username=username).first()

    if not target_user:
        flash('User not found!', 'danger')
        return redirect(url_for('main.chatrooms'))

    chatroom = ChatRoom.query.filter(
        ((ChatRoom.user1_id == current_user_obj.id) & (ChatRoom.user2_id == target_user.id)) |
        ((ChatRoom.user1_id == target_user.id) & (ChatRoom.user2_id == current_user_obj.id))
    ).first()

    if not chatroom:
        room_name = f"{current_user_obj.username}-{target_user.username}"
        chatroom = ChatRoom(room_name=room_name, user1_id=current_user_obj.id, user2_id=target_user.id)
        db.session.add(chatroom)
        db.session.commit()

    return redirect(url_for('main.personal_chat', room_id=chatroom.id))
