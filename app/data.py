import json
import os

DATA_FILE = "flashcards.json"

def load_data():
    """Load flashcards and stats from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"flashcards": [], "stats": {"correct": 0, "total": 0}}

def save_data(data):
    """Save flashcards and stats to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)