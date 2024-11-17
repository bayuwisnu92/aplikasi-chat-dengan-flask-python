# routes/group_routes.py

from flask import Blueprint, flash, redirect, render_template, request, jsonify, session, url_for
from app import db
from app.models import GroupInvitations, User, ChatRoomGrup, ChatGroupMember

group_bp = Blueprint('group', __name__)

# Route untuk mengundang pengguna ke grup
@group_bp.route('/invite_user', methods=['GET','POST'])
def invite_user():
    # Jika user mengakses halaman dengan GET, tampilkan form
    if request.method == 'GET':
        return render_template('invite_user.html')
    
    # Jika user mengirim form dengan POST, proses data form
    if request.method == 'POST':
        invited_by_user_id = session.get('user_id')
        if not invited_by_user_id:
            flash('Anda harus login untuk mengirim undangan', 'error')
            return redirect(url_for('invite_user'))
        
        chat_room_id = request.form.get('chat_room_id')
        invited_user_id = request.form.get('invited_user_id')

        # Validasi data yang dikirim
        if not chat_room_id or not invited_user_id:
            flash('Parameter tidak lengkap', 'error')
            return redirect(url_for('invite_user'))

        chat_room = ChatRoomGrup.query.get(chat_room_id)
        invited_user = User.query.get(invited_user_id)

        if not chat_room:
            flash('Chat room tidak ditemukan', 'error')
            return redirect(url_for('invite_user'))

        if not invited_user:
            flash('User tidak ditemukan', 'error')
            return redirect(url_for('invite_user'))

        # Simpan data undangan ke database
        new_invitation = GroupInvitations(
            chat_room_id=chat_room_id,
            invited_user_id=invited_user_id,
            invited_by_user_id=invited_by_user_id
        )
        db.session.add(new_invitation)
        db.session.commit()

        flash('Undangan berhasil dikirim', 'success')
        return redirect(url_for('group.invite_user'))

# Route untuk merespon undangan grup
@group_bp.route('/respond_invitation', methods=['GET','POST'])
def respond_invitation():
    if 'user_id' not in session:
        return jsonify({'error': 'Anda harus login untuk menanggapi undangan'}), 401

    invitation_id = request.json.get('invitation_id')
    response = request.json.get('response')  # 'accept' atau 'decline'

    invitation = GroupInvitations.query.get(invitation_id)

    if not invitation:
        return jsonify({'error': 'Undangan tidak ditemukan'}), 404

    if invitation.invited_user_id != session['user_id']:
        return jsonify({'error': 'Tidak berhak menanggapi undangan ini'}), 403

    if response == 'accept':
        invitation.status = 'accepted'
        new_member = ChatGroupMember(
            chat_room_id=invitation.chat_room_id,
            user_id=invitation.invited_user_id
        )
        db.session.add(new_member)
    else:
        invitation.status = 'declined'

    db.session.commit()
    return jsonify({'message': f'Undangan {response}'}), 200
