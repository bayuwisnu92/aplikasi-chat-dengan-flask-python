import uuid
from app import db

class ChatRoomGrup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Pembuat grup
    
    is_public = db.Column(db.Boolean, default=True)
    creator = db.relationship('User', backref='created_groups')
    invite_token = db.Column(db.String(100), unique=True, default=lambda: str(uuid.uuid4()))
    def __repr__(self):
        return f"<ChatRoom {self.room_name}>"
