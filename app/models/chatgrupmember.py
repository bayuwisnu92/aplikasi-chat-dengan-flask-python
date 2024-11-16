from app import db

class ChatGroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('chat_room_grup.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # True jika user adalah admin

    user = db.relationship('User', backref='group_memberships')
    room = db.relationship('ChatRoomGrup', backref='members')

    def __repr__(self):
        return f"<ChatGroupMember user_id={self.user_id} room_id={self.room_id} is_admin={self.is_admin}>"
