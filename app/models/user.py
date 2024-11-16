from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gambar_filename = db.Column(db.String(100), nullable=True)  # Kolom gambar baru
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Menyimpan waktu pembuatan
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Waktu pembaruan

    # Relasi ke permintaan pertemanan
    # Relasi ke permintaan pertemanan yang dikirim
    sent_requests = db.relationship(
        'FriendRequest', 
        foreign_keys='FriendRequest.sender_id', 
        backref='request_sender', 
        lazy=True
    )
    
    # Relasi ke permintaan pertemanan yang diterima
    received_requests = db.relationship(
        'FriendRequest', 
        foreign_keys='FriendRequest.receiver_id', 
        backref='request_receiver', 
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.username}>"