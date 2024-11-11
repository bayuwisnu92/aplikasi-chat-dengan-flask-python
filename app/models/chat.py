from app import db
from datetime import datetime

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_filename = db.Column(db.String(100), nullable=True)  # Kolom gambar baru
    room_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('chats', lazy=True))
    room = db.relationship('ChatRoom', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f"<Chat {self.message}>"
