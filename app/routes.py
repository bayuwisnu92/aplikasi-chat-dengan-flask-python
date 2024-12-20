import datetime
from flask import Blueprint, app, current_app, render_template, request, redirect, url_for, flash, session, jsonify
from app.controllers.auth_controller import edit_user, index_register, index_login, index_logout
from app.models import User, ChatRoom, Chat
from app import allowed_file, db, socketio  # Import socketio
from flask_socketio import emit, join_room, leave_room
from sqlalchemy.orm import aliased
from sqlalchemy import func, or_
from werkzeug.utils import secure_filename  # Tambahkan ini untuk mengamankan nama file
import os  # Tambahkan ini untuk mengelola path file
import time

from app.models.chatgrup import ChatGrup
from app.models.chatgrupmember import ChatGroupMember
from app.models.chatroomgrup import ChatRoomGrup
from app.models.friendrequest import FriendRequest  # Tambahkan ini untuk mendapatkan waktu saat ini





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


def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None
# Route untuk chatroom
@main.route('/', methods=['GET'])
def chatrooms():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user_id = session.get('user_id')
    username = session.get('username')
    current_user = get_current_user()
    if not current_user:
        flash("Silakan login terlebih dahulu.", "danger")
        return redirect(url_for('auth.login'))
    # Ambil informasi profil pengguna saat ini
    profile = User.query.filter_by(id=user_id).first()
    current_user = get_current_user()
    
    # Ambil semua pengguna kecuali pengguna saat ini
    users = User.query.join(
        FriendRequest, 
        or_(
            (FriendRequest.sender_id == current_user.id) & (FriendRequest.receiver_id == User.id),
            (FriendRequest.receiver_id == current_user.id) & (FriendRequest.sender_id == User.id)
        )
    ).filter(FriendRequest.status == 'accepted').all()
    
    # Ambil chatroom yang terkait dengan pengguna
    chatrooms = ChatRoom.query.filter(
        (ChatRoom.user1_id == user_id) | (ChatRoom.user2_id == user_id)
    ).all()
    
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

    # Mendapatkan daftar grup yang diikuti oleh user
    user_rooms = ChatGroupMember.query.filter_by(user_id=user_id).all()
    user_room_ids = [room.room_id for room in user_rooms]  # Ambil ID room yang diikuti user

    # Subquery untuk mendapatkan pesan terakhir di setiap chatroom yang diikuti oleh user
    last_message_subquery_grup = db.session.query(
        ChatGrup.room_id,
        func.max(ChatGrup.timestamp).label('last_timestamp')
    ).filter(ChatGrup.room_id.in_(user_room_ids)).group_by(ChatGrup.room_id).subquery()  # Hanya grup yang diikuti user

    # Alias untuk tabel ChatGrup agar lebih mudah diakses
    last_message_alias_grup = aliased(ChatGrup)

    # Query utama untuk mendapatkan chatroom yang diikuti user dan pesan terakhir
    grup_chatroom = ChatRoomGrup.query.filter(ChatRoomGrup.id.in_(user_room_ids)).all()

    last_messages_grup = db.session.query(
        ChatRoomGrup,
        last_message_alias_grup
    ).join(
        last_message_subquery_grup, ChatRoomGrup.id == last_message_subquery_grup.c.room_id
    ).join(
        last_message_alias_grup,
        (last_message_alias_grup.room_id == last_message_subquery_grup.c.room_id) &
        (last_message_alias_grup.timestamp == last_message_subquery_grup.c.last_timestamp)
    ).filter(
        ChatRoomGrup.id.in_(user_room_ids)  # Filter hanya untuk grup yang diikuti user
    ).order_by(last_message_alias_grup.timestamp.desc()).all()  # Mengurutkan berdasarkan timestamp terbaru

    # Membuat dictionary pesan terakhir untuk setiap pengguna
    last_messages_dict_grup = {}
    for chatroom, message in last_messages_grup:
        last_messages_dict_grup[chatroom.id] = message
    # Ambil grup yang publik dan belum diikuti oleh user saat ini
    joined_groups = db.session.query(ChatGroupMember.room_id).filter_by(user_id=user_id).all()
    joined_group_ids = [room_id for (room_id,) in joined_groups]

    public_rooms = ChatRoomGrup.query.filter(
        ChatRoomGrup.is_public == True,
        ~ChatRoomGrup.id.in_(joined_group_ids)
    ).all()
    # Filter pengguna yang tidak sama dengan pengguna saat ini dan tidak berteman
    users_bukan = User.query.filter(
    User.id != current_user.id
    ).filter(
        ~User.id.in_(
            db.session.query(FriendRequest.receiver_id)
            .filter(FriendRequest.sender_id == current_user.id, FriendRequest.status == 'accepted')
        )
    ).filter(
        ~User.id.in_(
            db.session.query(FriendRequest.sender_id)
            .filter(FriendRequest.receiver_id == current_user.id, FriendRequest.status == 'accepted')
        )
    ).all()
    title = 'chatroom'
    return render_template(
        'chatroom/chatrooms.html', 
        users=users, 
        username=username, 
        chatrooms=chatrooms, 
        last_messages=last_messages_dict, 
        title=title, 
        profile=profile,
        user_rooms=user_rooms,
        last_messages_grup=last_messages_dict_grup,
        grup_chatroom=grup_chatroom,
        public_rooms=public_rooms,
        users_bukan=users_bukan,
        current_user=current_user


    )

#membuat grup chatroom

@main.route('/create_chatroom', methods=['GET', 'POST'])
def create_chatroom():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user_id = session.get('user_id')
    username = session.get('username')
    title = 'Create Chatroom'

    if request.method == 'POST':
        room_name = request.form['room_name']

        # Buat chatroom baru
        new_chatroom = ChatRoomGrup(room_name=room_name, created_by=user_id)
        db.session.add(new_chatroom)
        db.session.commit()

        # Tambahkan pembuat sebagai admin di ChatGroupMember
        new_member = ChatGroupMember(user_id=user_id, room_id=new_chatroom.id, is_admin=True)
        db.session.add(new_member)
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

    # Periksa apakah user adalah anggota grup
    member = ChatGroupMember.query.filter_by(user_id=user_id, room_id=room_id).first()
    if not member:
        flash('You are not a member of this chat room.', 'danger')
        return redirect(url_for('main.chatrooms'))
    
    
    
    is_admin = member.is_admin if member else False

    messages = ChatGrup.query.filter_by(room_id=room_id).order_by(ChatGrup.timestamp).all()
    title = 'Chatroom Grup ' + chatroom.room_name

    return render_template('chatroom/grup_chat.html', chatroom=chatroom, messages=messages, username=username, title=title, is_admin=is_admin)


@socketio.on('send_message')
def handle_send_message(data):
    user_id = session.get('user_id')
    if not user_id:
        print("User tidak login.")
        return

    room_id = data.get('room_id')
    message_content = data.get('message', '').strip()
    image_filename = None
    is_group_chat = data.get('is_group_chat', False)

    print(f"Data diterima: {data}")
    print(f"user_id: {user_id}, room_id: {room_id}, is_group_chat: {is_group_chat}")

    # Validasi apakah pesan atau gambar kosong
    if not message_content and not data.get('image'):
        print("Pesan kosong, tidak dikirim.")
        return

    # Simpan gambar jika ada
    if data.get('image'):
        try:
            # Validasi format gambar
            if not data['image'].startswith('data:image/'):
                print("Format gambar tidak valid.")
                return
            
            # Hilangkan prefix base64 dan simpan gambar
            image_data = data['image'].split(',')[1]
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            image_filename = secure_filename(f"{user_id}_{int(time.time())}.png")
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)
            print(f"Gambar berhasil disimpan di {image_path}")
        except Exception as e:
            print(f"Error saat menyimpan gambar: {e}")
            return

    # Validasi dan buat pesan berdasarkan tipe chat
    if is_group_chat:
        chat_room = ChatRoomGrup.query.get(room_id)
        if not chat_room:
            print(f"Chat room grup dengan ID {room_id} tidak ditemukan.")
            return

        # Validasi keanggotaan grup
        is_member = ChatGroupMember.query.filter_by(room_id=room_id, user_id=user_id).first()
        if not is_member:
            print(f"User {user_id} bukan anggota grup {room_id}.")
            return

        new_message = ChatGrup(
            user_id=user_id,
            room_id=room_id,
            message=message_content,
            image_filename=image_filename,
            timestamp=datetime.datetime.utcnow()
        )
    else:
        chat_room = ChatRoom.query.get(room_id)
        if not chat_room:
            print(f"Chat room personal dengan ID {room_id} tidak ditemukan.")
            return

        new_message = Chat(
            user_id=user_id,
            room_id=room_id,
            message=message_content,
            image_filename=image_filename,
            timestamp=datetime.datetime.utcnow()
        )

    # Simpan pesan ke database
    try:
        db.session.add(new_message)
        db.session.commit()
        print("Pesan berhasil disimpan ke database.")
    except Exception as e:
        db.session.rollback()
        print(f"Error saat menyimpan pesan: {e}")
        return

    # Emit pesan ke klien berdasarkan tipe chat
    emit_data = {
        'message_id': new_message.id,
        'user_id': user_id,
        'username': session.get('username'),
        'message': message_content,
        'image_filename': image_filename,
        'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }

    if is_group_chat:
        emit('receive_message_grup', emit_data, room=room_id)
        # Emit update pesan terakhir untuk grup
        emit('update_last_messages_grup', {
            'room_id': room_id,
            'message': message_content,
            'username': session.get('username'),
            'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, broadcast=True)
    else:
        emit('receive_message', emit_data, room=room_id)
        # Emit update pesan terakhir untuk personal
        emit('update_last_messages', {
            'user_id': user_id,
            'message': message_content,
            'username': session.get('username'),
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
@main.route('/edit_message_grup/<int:message_id>', methods=['GET', 'POST'])
def edit_message_grup(message_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user_id = session.get('user_id')
    new_content = request.form.get('message_content')
    
    # Dapatkan pesan yang ingin diedit
    message = ChatGrup.query.get_or_404(message_id)

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



@main.route('/delete_message_grup/<int:message_id>', methods=['POST'])
def delete_message_grup(message_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    user_id = session.get('user_id')
    message = ChatGrup.query.get_or_404(message_id)

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

@main.route('/join_group/<int:room_id>', methods=['POST'])
def join_group_satu(room_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user_id = session.get('user_id')

    # Cek apakah user sudah menjadi anggota
    existing_member = ChatGroupMember.query.filter_by(user_id=user_id, room_id=room_id).first()
    if existing_member:
        flash('You are already a member of this group.', 'info')
    else:
        # Tambah user ke grup
        new_member = ChatGroupMember(user_id=user_id, room_id=room_id)
        db.session.add(new_member)
        db.session.commit()
        flash('Successfully joined the group.', 'success')

    return redirect(url_for('main.grup_chat', room_id=room_id))
@main.route('/search_user')
def search_user():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])  # Kembalikan daftar kosong jika query kosong

    # Cari pengguna berdasarkan username atau email
    users = User.query.filter(
        (User.username.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
    ).all()

    # Konversi hasil ke format JSON
    user_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(user_data)

@main.route('/group/<int:room_id>/invite_link', methods=['GET'])
def generate_invite_link(room_id):
    # Cek apakah user sudah login
    user_id = session.get('user_id')
    if not user_id:
        flash('Anda harus login terlebih dahulu', 'error')
        return redirect(url_for('login'))

    # Cek apakah grup dengan room_id ada
    group = ChatRoomGrup.query.get(room_id)
    if not group:
        flash('Grup tidak ditemukan', 'error')
        return redirect(url_for('home'))

    # Cek apakah user adalah admin grup
    is_admin = ChatGroupMember.query.filter_by(user_id=user_id, room_id=room_id, is_admin=True).first()
    if not is_admin:
        flash('Anda tidak memiliki akses untuk membuat link undangan grup ini', 'error')
        return redirect(url_for('home'))

    # Generate link undangan
    invite_link = f"http://127.0.0.1:5000/group/join/{group.invite_token}"

    # Render halaman untuk menampilkan link undangan
    return render_template('invite_link.html', invite_link=invite_link)


@main.route('/group/join/<invite_token>', methods=['GET'])
def join_group(invite_token):
    user_id = session.get('user_id')
    if not user_id:
        flash('Anda harus login terlebih dahulu', 'error')
        return redirect(url_for('login'))

    # Cari grup berdasarkan token
    group = ChatRoomGrup.query.filter_by(invite_token=invite_token).first()

    if not group:
        flash('Link undangan tidak valid', 'error')
        return redirect(url_for('main.chatrooms'))

    # Cek apakah user sudah menjadi anggota
    member = ChatGroupMember.query.filter_by(user_id=user_id, room_id=group.id).first()
    if member:
        flash('Anda sudah bergabung di grup ini', 'info')
        return redirect(url_for('main.chatrooms', group_id=group.id))

    # Tambahkan user sebagai anggota baru
    new_member = ChatGroupMember(user_id=user_id, room_id=group.id)  # Menggunakan room_id
    db.session.add(new_member)
    db.session.commit()

    flash('Berhasil bergabung ke grup!', 'success')
    return redirect(url_for('main.chatrooms', group_id=group.id))

