import os
from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from app.forms import RegistrationForm, LoginForm
from app.models.user import User
from app import db, bcrypt
def index_register():
    if 'user_id' in session:
        flash('Anda sudah login!', 'info')
        return redirect(url_for('main.chatrooms'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Akun Anda telah dibuat! Silakan login.', 'success')
        return redirect(url_for('main.login'))
    title = 'Register'
    return render_template('auth/register.html',form=form, title=title)


def index_login():
    if 'user_id' in session:
        flash('Anda sudah login!', 'info')
        return redirect(url_for('main.chatrooms'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Set user_id in session
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login berhasil!', 'success')
            return redirect(url_for('main.chatrooms'))
        else:
            flash('Login gagal. Cek email dan password.', 'danger')
        
    title = 'Login'
    return render_template('auth/login.html', form=form, title=title) 

def index_logout():
    session.clear()  # Menghapus semua data sesi
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('main.login'))

def edit_user():
    user_id = session.get('user_id')
    if not user_id:
        flash('Anda harus login terlebih dahulu')
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    if not user:
        flash('User tidak ditemukan')
        return redirect(url_for('main.login'))

    if 'profile_picture' not in request.files:
        flash('Tidak ada file yang dipilih')
        return redirect(request.url)

    file = request.files['profile_picture']
    if file.filename == '':
        flash('Nama file kosong')
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        profile_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile_pics')
        
        # Buat folder profile_pics jika belum ada
        if not os.path.exists(profile_folder):
            os.makedirs(profile_folder)
        
        filepath = os.path.join(profile_folder, filename)
        file.save(filepath)

        # Perbarui kolom gambar_filename pada user yang sedang login
        user.gambar_filename = f"profile_pics/{filename}"  # Simpan path relatif untuk akses yang mudah
        db.session.commit()
        flash('Foto profil berhasil diperbarui')
        return redirect(url_for('main.chatrooms'))  # Sesuaikan route 'profile' untuk halaman profil

    flash('Gagal mengunggah file')
    return redirect(request.url)

