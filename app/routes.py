import datetime
from flask import Blueprint, app, current_app, render_template, request, redirect, url_for, flash, session, jsonify
from app.controllers.auth_controller import edit_user, index_register, index_login, index_logout
from app.models import User, ChatRoom, Chat
from app import allowed_file, db, socketio  # Import socketio
from flask_socketio import emit, join_room, leave_room
from sqlalchemy.orm import aliased
from sqlalchemy import func
from werkzeug.utils import secure_filename  # Tambahkan ini untuk mengamankan nama file
import os  # Tambahkan ini untuk mengelola path file
import time

from app.models.chatgrup import ChatGrup
from app.models.chatroomgrup import ChatRoomGrup  # Tambahkan ini untuk mendapatkan waktu saat ini





main = Blueprint('main', __name__)

# Route untuk autentikasi
@main.route('/login', methods=['GET', 'POST'])
def login():
    return index_login()

@main.route('/register', methods=['GET', 'POST'])
def register():
    return index_register()

@main.route('/logout')
def logout():
    return index_logout()

# Route untuk profil
@main.route('/profile/<username>')
def profile(username):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user_id = session.get('user_id')
    session_username = session.get('username')
    title = 'profil'
    users = User.query.filter_by(username=username).first()
    return render_template('profile.html', title=title, users=users, username=session_username)

@main.route('/profile/edit_profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    username= session.get('username')
    
    return render_template('auth/update.html',username=username)

@main.route('/update_profile_picture', methods=['POST'])
def update_profile_picture():
    return edit_user()

# Route untuk chatroom
@main.route('/', methods=['GET'])
def chatrooms():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Ambil informasi profil pengguna saat ini
    profile = User.query.filter_by(id=user_id).first()
    
    # Ambil semua pengguna kecuali pengguna saat ini
    users = User.query.filter(User.id != user_id).all()

    # Ambil chatroom yang terkait dengan pengguna
    chatrooms = ChatRoom.query.filter(
        (ChatRoom.user1_id == user_id) | (ChatRoom.user2_id == user_id)
    ).all()
    grup_chatroom=ChatRoomGrup.query.all()
    # Subquery untuk mendapatkan pesan terakhir di setiap chatroom
    last_message_subquery = db.session.query(
        Chat.room_id,
        func.max(Chat.timestamp).label('last_timestamp')
    ).group_by(Chat.room_id).subquery()

    # Alias untuk tabel Chat agar lebih mudah diakses
    last_message_alias = aliased(Chat)

    # Query utama untuk mendapatkan chatroom dan pesan terakhir
    last_messages = db.session.query(
        ChatRoom,
        last_message_alias
    ).join(
        last_message_subquery, ChatRoom.id == last_message_subquery.c.room_id
    ).join(
        last_message_alias,
        (last_message_alias.room_id == last_message_subquery.c.room_id) &
        (last_message_alias.timestamp == last_message_subquery.c.last_timestamp)
    ).filter(
        (ChatRoom.user1_id == user_id) | (ChatRoom.user2_id == user_id)
    ).order_by(last_message_alias.timestamp.desc()).all()  # Mengurutkan berdasarkan timestamp terbaru

    # Membuat dictionary pesan terakhir untuk setiap pengguna
    last_messages_dict = {}
    for chatroom, message in last_messages:
        if chatroom.user1_id != user_id:
            last_messages_dict[chatroom.user1_id] = message
        if chatroom.user2_id != user_id:
            last_messages_dict[chatroom.user2_id] = message

    # Urutkan `users` berdasarkan timestamp pesan terakhir mereka (jika ada), default ke datetime.datetime.min jika None
    users = sorted(
        users, 
        key=lambda u: last_messages_dict.get(u.id, Chat()).timestamp or datetime.datetime.min, 
        reverse=True
    )

    title = 'chatroom'
    return render_template(
        'chatroom/chatrooms.html', 
        users=users, 
        username=username, 
        chatrooms=chatrooms, 
        last_messages=last_messages_dict, 
        title=title, 
        profile=profile,
        grup_chatroom=grup_chatroom
    )

#membuat grup chatroom

@main.route('/create_chatroom', methods=['GET','POST'])
def create_chatroom():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user_id = session.get('user_id')
    username = session.get('username')
    title = 'create_chatroom'
    if request.method == 'POST':
        user_id = session.get('user_id')
        username = session.get('username')
        room_name = request.form['room_name']
        new_chatroom = ChatRoomGrup(room_name=room_name)
        db.session.add(new_chatroom)
        db.session.commit()
        flash('Chatroom created successfully.', 'success')
        return redirect(url_for('main.chatrooms'))
    return render_template('chatroom/create_chatroom.html', title=title, username=username)


@main.route('/create_private_chat/<username>', methods=['GET', 'POST'])
def create_private_chat(username):
    # Mendapatkan ID pengguna saat ini dari sesi
    current_user_id = session.get('user_id')
    # Mengambil objek pengguna saat ini dari database
    current_user_obj = User.query.get(current_user_id)
    # Mencari pengguna target berdasarkan username yang diberikan
    target_user = User.query.filter_by(username=username).first()

    # Jika pengguna target tidak ditemukan, tampilkan pesan kesalahan dan redirect ke chatrooms
    if not target_user:
        flash('User not found!', 'danger')
        return redirect(url_for('main.chatrooms'))

    # Mencari chatroom yang sudah ada antara pengguna saat ini dan pengguna target
    chatroom = ChatRoom.query.filter(
        ((ChatRoom.user1_id == current_user_obj.id) & (ChatRoom.user2_id == target_user.id)) |
        ((ChatRoom.user1_id == target_user.id) & (ChatRoom.user2_id == current_user_obj.id))
    ).first()

    # Jika chatroom belum ada, buat chatroom baru
    if not chatroom:
        # Membuat nama chatroom berdasarkan username kedua pengguna
        room_name = f"{current_user_obj.username}-{target_user.username}"
        # Membuat objek ChatRoom baru
        chatroom = ChatRoom(room_name=room_name, user1_id=current_user_obj.id, user2_id=target_user.id)
        # Menambahkan chatroom baru ke database
        db.session.add(chatroom)
        db.session.commit()

    # Redirect ke halaman chat pribadi dengan ID chatroom yang baru dibuat atau yang sudah ada
    return redirect(url_for('main.personal_chat', room_id=chatroom.id))

@main.route('/chat/<int:room_id>', methods=['GET', 'POST'])
def personal_chat(room_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user_id = session.get('user_id')
    username = session.get('username')
    chatroom = ChatRoom.query.get_or_404(room_id)

    if user_id not in [chatroom.user1_id, chatroom.user2_id]:
        flash('You do not have permission to access this chatroom.', 'danger')
        return redirect(url_for('main.chatrooms'))

    messages = Chat.query.filter_by(room_id=room_id).order_by(Chat.timestamp).all()
    title = 'chatroom ' + chatroom.room_name

    return render_template('chatroom/personal_chat.html', chatroom=chatroom, messages=messages, username=username, title=title)
@main.route('/grup/<int:room_id>', methods=['GET', 'POST'])
def grup_chat(room_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user_id = session.get('user_id')
    username = session.get('username')
    chatroom = ChatRoomGrup.query.get_or_404(room_id)


    messages = ChatGrup.query.filter_by(room_id=room_id).order_by(ChatGrup.timestamp).all()
    title = 'chatroom grup ' + chatroom.room_name

    return render_template('chatroom/grup_chat.html', chatroom=chatroom, messages=messages, username=username, title=title)

@socketio.on('send_message')
def handle_send_message(data):
    user_id = session.get('user_id')
    room_id = data.get('room_id')
    message_content = data.get('message', '').strip()
    image_filename = None
    is_group_chat = data.get('is_group_chat', False)  # Identifikasi apakah pesan grup atau personal

    # Cek jika pesan kosong
    if not message_content and not data.get('image'):
        print("Pesan kosong, tidak dikirim.")
        return  # Hentikan proses jika pesan kosong

    # Simpan gambar jika dikirim dalam format base64
    if data.get('image'):
        import base64
        from io import BytesIO
        from PIL import Image
        import time
        import os

        image_data = data['image'].split(',')[1]  # Hilangkan bagian 'data:image/...;base64,'
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        image_filename = secure_filename(f"{user_id}_{int(time.time())}.png")
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)

        try:
            image.save(image_path)
            print(f"Image saved to {image_path}")
        except Exception as e:
            print(f"Error saving image: {e}")

    # Tentukan tabel yang digunakan berdasarkan jenis pesan
    if is_group_chat:
        # Simpan pesan grup
        new_message = ChatGrup(user_id=user_id, room_id=room_id, message=message_content, image_filename=image_filename)
    else:
        # Simpan pesan personal
        new_message = Chat(user_id=user_id, room_id=room_id, message=message_content, image_filename=image_filename)

    # Simpan ke database
    db.session.add(new_message)
    db.session.commit()

    # Emit pesan ke klien di room untuk menampilkan pesan baru
    emit('receive_message', {
        'message_id': new_message.id,
        'user_id': user_id,
        'username': session.get('username'),
        'message': message_content,
        'image_filename': image_filename,
        'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }, room=room_id)

    # Emit event `update_last_messages` ke semua klien untuk memperbarui pesan terakhir
    emit('update_last_messages', {
        'user_id': user_id,
        'message': message_content,
        'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }, broadcast=True)







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

# Route untuk mengedit dan menghapus pesan
@main.route('/edit_message/<int:message_id>', methods=['GET', 'POST'])
def edit_message(message_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user_id = session.get('user_id')
    new_content = request.form.get('message_content')
    
    # Dapatkan pesan yang ingin diedit
    message = Chat.query.get_or_404(message_id)

    # Pastikan hanya pemilik pesan yang bisa mengeditnya
    if message.user_id != user_id:
        flash("You don't have permission to edit this message.", "danger")
        return redirect(url_for('main.personal_chat', room_id=message.room_id))

    # Update isi pesan dan simpan ke database
    message.message = new_content
    db.session.commit()

    # Kirim pembaruan pesan ke pengguna lain di room yang sama tanpa 'broadcast'
    socketio.emit('edit_message', {
        'message_id': message_id,
        'new_content': new_content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }, room=message.room_id)

    flash("Message updated successfully!", "success")
    return redirect(url_for('main.personal_chat', room_id=message.room_id))



@main.route('/delete_message/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user_id = session.get('user_id')
    message = Chat.query.get_or_404(message_id)

    # Pastikan hanya pemilik pesan yang bisa menghapusnya
    if message.user_id != user_id:
        flash("You don't have permission to delete this message.", "danger")
        return redirect(url_for('main.personal_chat', room_id=message.room_id))

    room_id = message.room_id
    
    # Hapus file gambar jika ada
    if message.image_filename:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], message.image_filename)
        try:
            os.remove(image_path)  # Menghapus file gambar dari server
            print(f"Image {image_path} deleted successfully.")
        except Exception as e:
            print(f"Error deleting image: {e}")

    # Hapus pesan dari database
    db.session.delete(message)
    db.session.commit()

    # Emit event untuk menghapus pesan pada UI pengguna lain tanpa 'broadcast'
    socketio.emit('delete_message', {
        'message_id': message_id
    }, room=room_id)

    flash("Message deleted successfully!", "success")
    return redirect(url_for('main.personal_chat', room_id=room_id))

def login_required(func):
    """ Custom decorator to check if user is logged in via session. """
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper