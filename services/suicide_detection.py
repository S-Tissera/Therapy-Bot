def detect_suicidal_thoughts(user_input: str) -> bool:
    suicide_keywords = [
        "kill myself", "end my life", "suicide", "want to die",
        "can't go on", "life is meaningless", "no reason to live",
        "hurt myself", "die", "give up"
    ]
    lowered_input = user_input.lower()
    return any(phrase in lowered_input for phrase in suicide_keywords)

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
