import json
import os
import shutil
from datetime import datetime
import tempfile
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DATA_FILE = "flashcards.json"
BACKUP_DIR = "backups"
MAX_BACKUPS = 5

def ensure_backup_dir():
    """Ensure backup directory exists."""
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create backup directory: {e}")

def create_backup():
    """Create a backup of the current data file."""
    if not os.path.exists(DATA_FILE):
        return
    
    try:
        ensure_backup_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"flashcards_backup_{timestamp}.json")
        shutil.copy2(DATA_FILE, backup_file)
        cleanup_old_backups()
    except Exception as e:
        logging.warning(f"Could not create backup: {e}")

def cleanup_old_backups():
    """Remove old backup files, keeping only the most recent ones."""
    try:
        backup_files = [
            (os.path.join(BACKUP_DIR, f), os.path.getmtime(os.path.join(BACKUP_DIR, f)))
            for f in os.listdir(BACKUP_DIR)
            if f.startswith("flashcards_backup_") and f.endswith(".json")
        ]
        backup_files.sort(key=lambda x: x[1], reverse=True)
        for file_path, _ in backup_files[MAX_BACKUPS:]:
            try:
                os.remove(file_path)
            except Exception as e:
                logging.warning(f"Could not remove old backup {file_path}: {e}")
    except Exception as e:
        logging.warning(f"Could not cleanup old backups: {e}")

def load_data():
    """Load flashcards and stats from JSON file with error handling."""
    default_data = {
        "flashcards": [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is 2 + 2?", "answer": "4"},
            {"question": "What programming language is this app written in?", "answer": "Python"}
        ],
        "stats": {"correct": 0, "total": 0},
        "settings": {"default_time_limit": 10, "auto_save": True, "sound_enabled": True},
        "version": "2.1",
        "created": datetime.now().isoformat(),
        "last_modified": datetime.now().isoformat()
    }
    
    if not os.path.exists(DATA_FILE):
        try:
            save_data(default_data)
            return default_data
        except Exception as e:
            logging.error(f"Error creating default data file: {e}")
            return default_data
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return validate_and_migrate_data(data)
    except json.JSONDecodeError as e:
        logging.error(f"Corrupted data file: {e}")
        return load_backup_or_default(default_data)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return load_backup_or_default(default_data)

def load_backup_or_default(default_data):
    """Try to load from backup, or return default data."""
    try:
        ensure_backup_dir()
        backup_files = [
            (os.path.join(BACKUP_DIR, f), os.path.getmtime(os.path.join(BACKUP_DIR, f)))
            for f in os.listdir(BACKUP_DIR)
            if f.startswith("flashcards_backup_") and f.endswith(".json")
        ]
        if backup_files:
            backup_files.sort(key=lambda x: x[1], reverse=True)
            latest_backup = backup_files[0][0]
            with open(latest_backup, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logging.info(f"Loaded data from backup: {latest_backup}")
                return validate_and_migrate_data(data)
    except Exception as e:
        logging.error(f"Error loading backup: {e}")
    return default_data

def validate_and_migrate_data(data):
    """Validate data structure and migrate from older versions if needed."""
    if "flashcards" not in data:
        data["flashcards"] = []
    if "stats" not in data:
        data["stats"] = {"correct": 0, "total": 0}
    if "settings" not in data:
        data["settings"] = {"default_time_limit": 10, "auto_save": True, "sound_enabled": True}
    if "version" not in data:
        data["version"] = "2.1"
    if "created" not in data:
        data["created"] = datetime.now().isoformat()
    
    data["last_modified"] = datetime.now().isoformat()
    
    valid_flashcards = []
    for card in data["flashcards"]:
        if isinstance(card, dict) and "question" in card and "answer" in card:
            card["question"] = str(card["question"]).strip()
            card["answer"] = str(card["answer"]).strip()
            if card["question"] and card["answer"]:
                valid_flashcards.append(card)
    data["flashcards"] = valid_flashcards
    
    if not isinstance(data["stats"], dict):
        data["stats"] = {"correct": 0, "total": 0}
    if "correct" not in data["stats"] or not isinstance(data["stats"]["correct"], int):
        data["stats"]["correct"] = 0
    if "total" not in data["stats"] or not isinstance(data["stats"]["total"], int):
        data["stats"]["total"] = 0
    
    return data

def save_data(data):
    """Save flashcards and stats to JSON file with backup and error handling."""
    try:
        create_backup()
        data["last_modified"] = datetime.now().isoformat()
        temp_file = DATA_FILE + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        with open(temp_file, 'r', encoding='utf-8') as f:
            json.load(f)
        shutil.move(temp_file, DATA_FILE)
    except Exception as e:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        raise Exception(f"Failed to save data: {e}")

def get_data_info():
    """Get information about the current data file."""
    if not os.path.exists(DATA_FILE):
        return "No data file exists yet."
    
    try:
        data = load_data()
        flashcard_count = len(data.get("flashcards", []))
        stats = data.get("stats", {})
        created = data.get("created", "Unknown")
        last_modified = data.get("last_modified", "Unknown")
        version = data.get("version", "2.1")
        
        accuracy = (stats.get('correct', 0) / max(stats.get('total', 1), 1) * 100)
        info = f"""
Data File Information:
- File: {DATA_FILE}
- Version: {version}
- Flashcards: {flashcard_count}
- Total attempts: {stats.get('total', 0)}
- Correct answers: {stats.get('correct', 0)}
- Accuracy: {accuracy:.1f}%
- Created: {created}
- Last modified: {last_modified}
        """
        return info.strip()
    except Exception as e:
        return f"Error getting data info: {e}"

def export_data(export_path):
    """Export flashcards data to a specified file."""
    try:
        data = load_data()
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return f"Data exported successfully to {export_path}"
    except Exception as e:
        return f"Error exporting data: {e}"

def import_data(import_path):
    """Import flashcards data from a specified file."""
    try:
        with open(import_path, 'r', encoding='utf-8') as f:
            imported_data = json.load(f)
        validated_data = validate_and_migrate_data(imported_data)
        save_data(validated_data)
        return f"Data imported successfully from {import_path}"
    except Exception as e:
        return f"Error importing data: {e}"