import uuid
from datetime import datetime
from db.connection import get_db_connection

def create_user(is_anonymous=True):
    user_id = str(uuid.uuid4())
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (user_id, created_at, is_anonymous) VALUES (%s, %s, %s)",
                   (user_id, datetime.now(), is_anonymous))
    db.commit()
    cursor.close()
    db.close()
    return user_id

def start_conversation(user_id):
    conversation_id = str(uuid.uuid4())
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO conversations (conversation_id, user_id, started_at) VALUES (%s, %s, %s)",
                   (conversation_id, user_id, datetime.now()))
    db.commit()
    cursor.close()
    db.close()
    return conversation_id
