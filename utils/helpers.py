import time
import random

def calculate_response_delay(text: str) -> float:
    """Simulate human-like typing delay"""
    word_count = len(text.split())
    base_delay = 0.5
    per_word_delay = 0.2
    jitter = random.uniform(-0.1, 0.3)
    return max(0.3, base_delay + (word_count * per_word_delay) + jitter)

def generate_session_id() -> str:
    return f"session_{int(time.time())}_{random.randint(1000,9999)}"