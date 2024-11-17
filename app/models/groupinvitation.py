from datetime import datetime
from app import db

class GroupInvitations(db.Model):
    __tablename__ = 'group_invitations'
    id = db.Column(db.Integer, primary_key=True)
    chat_room_id = db.Column(db.Integer, db.ForeignKey('chat_room_grup.id'), nullable=False)
    invited_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'chat_room_id': self.chat_room_id,
            'invited_user_id': self.invited_user_id,
            'invited_by_user_id': self.invited_by_user_id,
            'status': self.status,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }