
from flask import render_template
from app.forms import RegistrationForm, LoginForm
from app.models.user import User
from app import db, bcrypt
from flask import session, redirect, url_for, flash

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