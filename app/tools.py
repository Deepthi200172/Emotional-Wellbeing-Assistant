import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def identify_emotion(text: str) -> str:
    text = text.lower()

    emotion_map = {
        "sad": "sadness",
        "lonely": "loneliness",
        "hurt": "hurt",
        "anxious": "anxiety",
        "worried": "anxiety",
        "scared": "anxiety",
        "angry": "anger",
        "confused": "confusion",
        "lost": "confusion",
        "stressed": "stress",
        "hopeless": "hopelessness",
        "guilty": "guilt",
        "shame": "shame",
    }

    for word, emo in emotion_map.items():
        if word in text:
            return emo

    return "mixed or unclear"


def suggest_coping_method(emotion: str) -> str:
    db_path = DATA_DIR / "coping_db.json"
    with db_path.open("r") as f:
        data = json.load(f)

    return random.choice(data.get(emotion, data["mixed or unclear"]))


def journaling_prompt(emotion: str) -> str:
    db_path = DATA_DIR / "journal_db.json"
    with db_path.open("r") as f:
        data = json.load(f)

    return random.choice(data.get(emotion, data["mixed or unclear"]))
