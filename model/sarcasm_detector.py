from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the model and tokenizer once
model_name = "helinivan/english-sarcasm-detector"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def detect_sarcasm(text: str) -> dict:
    """
    Args:
        text (str): The input sentence to analyze.

    Returns:
        dict: A dictionary with 'sarcasm' (bool) and 'confidence' (float between 0 and 1).
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    prediction = torch.argmax(probs, dim=1).item()
    confidence = round(probs[0][prediction].item(), 4)

    return {
        "sarcasm": bool(prediction),
        "confidence": confidence
    }


