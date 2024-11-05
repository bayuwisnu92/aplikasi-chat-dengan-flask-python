
from app import db

class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), unique=True, nullable=False)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user1 = db.relationship('User', foreign_keys=[user1_id], backref='user1_rooms')
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='user2_rooms')

    def __repr__(self):
        return f"<ChatRoom {self.room_name}>"
