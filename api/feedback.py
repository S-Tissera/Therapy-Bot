from flask import Blueprint, request, jsonify
from db.connection import get_db_connection
from datetime import datetime

feedback = Blueprint("feedback", __name__)

@feedback.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()

    user_id = data.get('user_id')
    emotion_id = data.get('emotion_id')
    is_correct = data.get('is_correct')  # Boolean: true if bot's emotion was correct
    corrected_emotion = data.get('corrected_emotion')  # Optional
    comment = data.get('comment')  # Optional
    timestamp = datetime.now()

    if user_id is None or emotion_id is None or is_correct is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO feedback (emotion_id, user_id, is_correct, corrected_emotion, comment, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (emotion_id, user_id, is_correct, corrected_emotion, comment, timestamp))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Feedback submitted successfully"}), 200
    except Exception as e:
        print("[ERROR] Feedback submission failed:", str(e))
        return jsonify({"error": str(e)}), 500
