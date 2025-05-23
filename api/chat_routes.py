from flask import Blueprint, request, jsonify
from model.emotion_roberta import detect_emotions
from model.sarcasm_detector import detect_sarcasm
from services.log_message import log_interaction
from services.session_manager import start_conversation
from model.response_model import generate_cohere_response
from db.connection import get_db_connection
import uuid
import datetime

chat = Blueprint("chat", __name__)

@chat.route("/chat", methods=["POST"])
def chat_with_bot():
    data = request.json
    user_input = data.get("message", "")
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        # 1. Detect emotion and sarcasm
        emotions = detect_emotions(user_input)
        top = max(emotions, key=lambda x: x["score"])
        emotion_label = top["label"]
        emotion_conf = top["score"]

        sarcasm_data = detect_sarcasm(user_input)
        is_sarcastic = sarcasm_data.get("sarcasm", False)
        sarcasm_conf = sarcasm_data.get("confidence", 0.0)

        # 2. Start or retrieve conversation
        conversation_id = start_conversation(user_id)

        # 3. Generate response
        response_text = generate_cohere_response(user_input, emotion_label, is_sarcastic)

        # 4. Generate UUIDs
        user_message_id = str(uuid.uuid4())
        emotion_id = str(uuid.uuid4())

        conn = get_db_connection()
        cursor = conn.cursor()

        # 5. Insert user message
        insert_user_message_sql = """
            INSERT INTO messages (message_id, conversation_id, sender, message_text, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_user_message_sql, (
            user_message_id,
            conversation_id,
            "user",
            user_input,
            datetime.datetime.utcnow()
        ))

        # 6. Insert emotion record
        insert_emotion_sql = """
            INSERT INTO emotions (emotion_id, message_id, primary_emotion, sarcasm_score, confidence)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_emotion_sql, (
            emotion_id,
            user_message_id,
            emotion_label,
            sarcasm_conf,
            emotion_conf
        ))

        # 7. Insert bot message
        bot_message_id = str(uuid.uuid4())
        insert_bot_message_sql = """
            INSERT INTO messages (message_id, conversation_id, sender, message_text, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_bot_message_sql, (
            bot_message_id,
            conversation_id,
            "bot",
            response_text,
            datetime.datetime.utcnow()
        ))

        # 8. Commit and close
        conn.commit()
        cursor.close()
        conn.close()

        # 9. Log interaction
        log_interaction(
            conversation_id,
            user_input,
            response_text,
            {"label": emotion_label, "score": emotion_conf},
            {"sarcasm": is_sarcastic, "confidence": sarcasm_conf}
        )

        return jsonify({
            "response": response_text,
            "emotion": emotion_label,
            "emotion_id": emotion_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
