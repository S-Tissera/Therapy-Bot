import mysql.connector

def get_recent_emotion_history(user_id, limit=5):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='chatbot_db'
    )
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        m.message_text,
        e.primary_emotion,
        m.created_at
    FROM messages m
    JOIN conversations c ON m.conversation_id = c.conversation_id
    LEFT JOIN emotions e ON m.message_id = e.message_id
    WHERE c.user_id = %s AND m.sender = 'user'
    ORDER BY m.created_at DESC
    LIMIT %s;

    """
    cursor.execute(query, (user_id, limit))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_emotional_trend(emotions):
    negative = {"sad", "frustrated", "angry", "depressed", "lonely"}
    recent_negatives = [e for e in emotions if e in negative]
    if len(recent_negatives) >= 3:
        return "The user has been consistently feeling down."
    return "The user's emotional state seems stable."

def context_snippet_from_messages(emotion_history):
    return "\n".join(
        [f"[{row['created_at']}] {row['message_text']}" for row in reversed(emotion_history)]
    )
