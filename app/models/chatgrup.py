from app import db
from datetime import datetime

class ChatGrup(db.Model):
    __tablename__ = 'chat_groups'  # Pastikan konsistensi nama tabel
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_filename = db.Column(db.String(100), nullable=True)  # Kolom gambar baru
    room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'), nullable=True)  # Sesuaikan nama tabel
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi dengan User dan ChatRoom
    user = db.relationship('User', backref='chat_grup_messages')
    room = db.relationship('ChatRoom', backref='chat_grup_messages')

    def __repr__(self):
        return f"<ChatGrup message={self.message}, user_id={self.user_id}>"
