from app import db

class ChatRoomGrup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<ChatRoom {self.room_name}>"
