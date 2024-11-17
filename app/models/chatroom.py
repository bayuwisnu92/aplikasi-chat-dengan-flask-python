from app import db

class ChatRoom(db.Model):
    __tablename__ = 'chat_rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), unique=True, nullable=False)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relasi untuk User 1 dan User 2
    user1 = db.relationship('User', foreign_keys=[user1_id], backref='chat_rooms_as_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='chat_rooms_as_user2')

    def __repr__(self):
        return f"<ChatRoom room_name={self.room_name}>"
