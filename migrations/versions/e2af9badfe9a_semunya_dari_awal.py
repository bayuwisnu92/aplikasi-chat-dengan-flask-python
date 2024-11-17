""" semunya dari awal 

Revision ID: e2af9badfe9a
Revises: 
Create Date: 2024-11-17 12:13:52.491332

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e2af9badfe9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_name', sa.String(length=100), nullable=False),
    sa.Column('user1_id', sa.Integer(), nullable=False),
    sa.Column('user2_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user1_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user2_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('room_name')
    )
    op.create_table('chat_groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('image_filename', sa.String(length=100), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['chat_rooms.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('chat_room', schema=None) as batch_op:
        batch_op.drop_index('room_name')

    op.drop_table('chat_room')
    op.drop_table('chat_grup')
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.drop_constraint('chat_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'chat_rooms', ['room_id'], ['id'])

    with op.batch_alter_table('chat_room_grup', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'user', ['created_by'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_room_grup', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('chat_ibfk_1', 'chat_room', ['room_id'], ['id'])

    op.create_table('chat_grup',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('image_filename', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('room_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('message', mysql.TEXT(), nullable=False),
    sa.Column('timestamp', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['room_id'], ['chat_room.id'], name='chat_grup_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='chat_grup_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('chat_room',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('room_name', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('user1_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('user2_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user1_id'], ['user.id'], name='chat_room_ibfk_1'),
    sa.ForeignKeyConstraint(['user2_id'], ['user.id'], name='chat_room_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('chat_room', schema=None) as batch_op:
        batch_op.create_index('room_name', ['room_name'], unique=True)

    op.drop_table('chat_groups')
    op.drop_table('chat_rooms')
    # ### end Alembic commands ###