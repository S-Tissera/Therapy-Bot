import os
import re
import cohere
from model.emotion_roberta import detect_emotions
from model.sarcasm_detector import detect_sarcasm
from services.session_manager import create_user, start_conversation
from services.log_message import log_interaction
from services.context_service import get_recent_emotion_history, get_emotional_trend, context_snippet_from_messages

# Suppress TensorFlow info logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

co = cohere.Client("sHTtYZWnFNFpfP7GEz353DrxGnEmfb8YWXv8gViF")

def detect_suicidal_thoughts(user_input: str) -> bool:
    """Check for suicide-related keywords with improved pattern matching"""
    cleaned_input = re.sub(r'[^\w\s]', '', user_input.lower())
    patterns = [
        r"\b(kill|ending|harm|hurt|take)\s*(my|meself|myself)\b",
        r"\b(suicide|suicidal|self\s*harm)\b",
        r"\b(die|dying|end\s*it\s*all)\b",
        r"\b(no\s+reason\s+to\s+live|can'?t\s+go\s+on)\b",
        r"\b(give\s+up|life\s+is\s+pointless)\b"
    ]
    return any(re.search(pattern, cleaned_input) for pattern in patterns)

def emergency_hotline_response() -> str:
    return (
        "I'm really sorry you're feeling this way. You're not alone, and there are people who care and want to help.\n\n"
        "**If you're in immediate danger, please talk to someone you trust or contact emergency services right away.**\n\n"
        "Here are some helplines you can reach out to:\n\n"
        "🇱🇰 **Sri Lanka Emergency Hotlines**:\n"
        "• CCCline - **1333** (free, confidential emotional support)\n"
        "• Sumithrayo - **+94 11 2696666** or [sumithrayo.org](http://www.sumithrayo.org)\n"
        "• National Mental Health Helpline - **1926** (24/7 support)\n\n"
        "🌐 **International Help**:\n"
        "• Visit [https://findahelpline.com/](https://findahelpline.com/) to find support services near you\n\n"
        "Please remember, you're not alone — there are people who want to support you through this."
    )

def generate_cohere_response(user_input: str, emotion: str, sarcasm: bool, trend_note: str = "", context_snippet: str = "") -> str:
    sarcasm_text = "sarcasm detected" if sarcasm else "no sarcasm"
    prompt = f"""
You are a compassionate and insightful therapist chatbot. Respond empathetically and thoughtfully.

User emotional trend: {trend_note}
Recent messages:
{context_snippet}

Current user state:
- Emotion: {emotion.upper()}
- Sarcasm: {sarcasm_text}

User said: "{user_input}"

Your therapeutic response:
"""
    response = co.generate(
        model="command-light",
        prompt=prompt,
        max_tokens=120,
        temperature=0.7
    )
    return response.generations[0].text.strip()

def main():
    print("Chatbot: Hello! Let's talk. Type 'exit' to end the conversation.\n")

    user_id = create_user(is_anonymous=True)
    conversation_id = start_conversation(user_id)

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        try:
            # Immediate suicide keyword check
            if detect_suicidal_thoughts(user_input):
                hotline_message = emergency_hotline_response()
                print("\n[Emergency Response Triggered]")
                print(f"\nChatbot: {hotline_message}\n")

                log_interaction(
                    conversation_id=conversation_id,
                    user_text=user_input,
                    bot_text=hotline_message,
                    emotion_data={"label": "crisis", "score": 1.0},
                    sarcasm_data={"sarcasm": False, "confidence": 1.0}
                )
                continue  # Skip to next iteration

            # Normal processing flow
            emotions = detect_emotions(user_input)
            top_emotion = max(emotions, key=lambda x: x["score"])
            emotion_label = top_emotion["label"]
            emotion_conf = top_emotion["score"]

            sarcasm_data = detect_sarcasm(user_input)
            is_sarcastic = sarcasm_data.get("sarcasm", False)
            sarcasm_conf = sarcasm_data.get("confidence", 0.0)

            # Context gathering
            emotion_history = get_recent_emotion_history(user_id)
            emotion_trend = get_emotional_trend([e["primary_emotion"] for e in emotion_history])
            context_snippet = context_snippet_from_messages(emotion_history)

            # Generate Cohere response
            bot_reply = generate_cohere_response(
                user_input=user_input,
                emotion=emotion_label,
                sarcasm=is_sarcastic,
                trend_note=emotion_trend,
                context_snippet=context_snippet
            )

            # Logging and output
            log_interaction(
                conversation_id=conversation_id,
                user_text=user_input,
                bot_text=bot_reply,
                emotion_data={"label": emotion_label, "score": emotion_conf},
                sarcasm_data={"sarcasm": is_sarcastic, "confidence": sarcasm_conf}
            )

            print(f"\nChatbot: {bot_reply}\n")
            print(f"[System] Emotion: {emotion_label} ({emotion_conf:.2f}), "
                  f"Sarcasm: {is_sarcastic} ({sarcasm_conf:.2f})\n")

        except Exception as e:
            print(f"\n[Error] {str(e)}\n")
            continue

if __name__ == "__main__":
    main()