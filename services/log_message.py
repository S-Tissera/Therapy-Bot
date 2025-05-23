import uuid
from datetime import datetime
from db.connection import get_db_connection

def log_interaction(conversation_id, user_text, bot_text, emotion_data, sarcasm_data):
    db = get_db_connection()
    cursor = db.cursor()

    user_msg_id = str(uuid.uuid4())
    bot_msg_id = str(uuid.uuid4())
    emotion_id = str(uuid.uuid4())
    response_id = str(uuid.uuid4())

    now = datetime.now()

    # Insert user message
    cursor.execute("""
        INSERT INTO messages (message_id, conversation_id, sender, message_text, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_msg_id, conversation_id, 'user', user_text, now))

    # Insert bot response
    cursor.execute("""
        INSERT INTO messages (message_id, conversation_id, sender, message_text, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (bot_msg_id, conversation_id, 'bot', bot_text, now))

    # Insert emotion and sarcasm data
    cursor.execute("""
        INSERT INTO emotions (emotion_id, message_id, primary_emotion, sarcasm_score, confidence)
        VALUES (%s, %s, %s, %s, %s)
    """, (emotion_id, user_msg_id, emotion_data['label'], sarcasm_data['sarcasm'], emotion_data['score']))

    # Insert bot response mapping
    cursor.execute("""
        INSERT INTO responses (response_id, message_id, response_text)
        VALUES (%s, %s, %s)
    """, (response_id, bot_msg_id, bot_text))

    db.commit()
    cursor.close()
    db.close()
