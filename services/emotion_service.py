from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Pretrained emotion model (GoEmotions fine-tuned)
EMOTION_MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

tokenizer = AutoTokenizer.from_pretrained(EMOTION_MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(EMOTION_MODEL_NAME)

# Pipeline for emotion classification
emotion_classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    return_all_scores=True
)

def detect_emotions(text: str):
    """
    Predicts emotion scores for the input text.
    Returns a list of dicts: [{'label': str, 'score': float}, ...]
    """
    # The pipeline returns a list of per-sample results (lists of dicts), so we extract the first element
    results = emotion_classifier(text)
    if isinstance(results, list) and len(results) > 0:
        # If return_all_scores=True, each entry is a list of dicts
        first = results[0]
        if isinstance(first, list):
            return first
        return results
    return []

