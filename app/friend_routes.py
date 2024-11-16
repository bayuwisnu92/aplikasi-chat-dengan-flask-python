# friend_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, session
from app import db
from app.models import User, FriendRequest

friend_bp = Blueprint('friend', __name__)

# Helper function untuk mendapatkan pengguna yang sedang login
def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

# Daftar pengguna lain
@friend_bp.route('/users')

def user_list():
    current_user = get_current_user()
    if not current_user:
        flash("Silakan login terlebih dahulu.", "danger")
        return redirect(url_for('auth.login'))
    username = current_user.username

    users = User.query.filter(User.id != current_user.id).all()
    
    return render_template('user_list.html', users=users, current_user=current_user, username=username)

# Kirim Permintaan Pertemanan
@friend_bp.route('/send_request/<int:receiver_id>', methods=['POST'])
def send_request(receiver_id):
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('auth.login'))

    existing_request = FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=receiver_id).first()
    if not existing_request:
        new_request = FriendRequest(sender_id=current_user.id, receiver_id=receiver_id)
        db.session.add(new_request)
        db.session.commit()
        flash("Permintaan pertemanan berhasil dikirim!", "success")
    else:
        flash("Permintaan pertemanan sudah dikirim sebelumnya!", "info")

    return redirect(url_for('friend.user_list'))

# Terima Permintaan Pertemanan
@friend_bp.route('/accept_request/<int:request_id>', methods=['POST'])
def accept_request(request_id):
    current_user = get_current_user()
    friend_request = FriendRequest.query.get(request_id)
    if friend_request and friend_request.receiver_id == current_user.id:
        friend_request.status = 'accepted'
        db.session.commit()
        flash("Permintaan pertemanan diterima!", "success")
    return redirect(url_for('friend.user_list'))

# Tolak Permintaan Pertemanan
@friend_bp.route('/reject_request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    current_user = get_current_user()
    friend_request = FriendRequest.query.get(request_id)
    if friend_request and friend_request.receiver_id == current_user.id:
        friend_request.status = 'rejected'
        db.session.commit()
        flash("Permintaan pertemanan ditolak!", "info")
    return redirect(url_for('friend.user_list'))
