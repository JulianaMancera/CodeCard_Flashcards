import json
import os
import shutil
from datetime import datetime
import tempfile

DATA_FILE = "flashcards.json"
BACKUP_DIR = "backups"
MAX_BACKUPS = 5

def ensure_backup_dir():
    """Ensure backup directory exists."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def create_backup():
    """Create a backup of the current data file."""
    if not os.path.exists(DATA_FILE):
        return
    
    try:
        ensure_backup_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"flashcards_backup_{timestamp}.json")
        shutil.copy2(DATA_FILE, backup_file)
        
        # Clean up old backups
        cleanup_old_backups()
        
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")

def cleanup_old_backups():
    """Remove old backup files, keeping only the most recent ones."""
    try:
        backup_files = []
        for file in os.listdir(BACKUP_DIR):
            if file.startswith("flashcards_backup_") and file.endswith(".json"):
                file_path = os.path.join(BACKUP_DIR, file)
                backup_files.append((file_path, os.path.getmtime(file_path)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups beyond MAX_BACKUPS
        for file_path, _ in backup_files[MAX_BACKUPS:]:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Warning: Could not remove old backup {file_path}: {e}")
                
    except Exception as e:
        print(f"Warning: Could not cleanup old backups: {e}")

def load_data():
    """Load flashcards and stats from JSON file with error handling."""
    default_data = {
        "flashcards": [
            {
                "question": "What is the capital of France?",
                "answer": "Paris"
            },
            {
                "question": "What is 2 + 2?",
                "answer": "4"
            },
            {
                "question": "What programming language is this app written in?",
                "answer": "Python"
            }
        ],
        "stats": {
            "correct": 0,
            "total": 0
        },
        "settings": {
            "default_time_limit": 10,
            "auto_save": True,
            "sound_enabled": True
        },
        "version": "2.0",
        "created": datetime.now().isoformat(),
        "last_modified": datetime.now().isoformat()
    }
    
    if not os.path.exists(DATA_FILE):
        # Create default data file
        try:
            save_data(default_data)
            return default_data
        except Exception as e:
            print(f"Error creating default data file: {e}")
            return default_data
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Validate and migrate data structure if needed
        data = validate_and_migrate_data(data)
        return data
        
    except json.JSONDecodeError as e:
        print(f"Error: Corrupted data file. {e}")
        return load_backup_or_default(default_data)
    except Exception as e:
        print(f"Error loading data: {e}")
        return load_backup_or_default(default_data)

def load_backup_or_default(default_data):
    """Try to load from backup, or return default data."""
    try:
        ensure_backup_dir()
        backup_files = []
        
        for file in os.listdir(BACKUP_DIR):
            if file.startswith("flashcards_backup_") and file.endswith(".json"):
                file_path = os.path.join(BACKUP_DIR, file)
                backup_files.append((file_path, os.path.getmtime(file_path)))
        
        if backup_files:
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Try to load the most recent backup
            latest_backup = backup_files[0][0]
            with open(latest_backup, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Loaded data from backup: {latest_backup}")
                return validate_and_migrate_data(data)
                
    except Exception as e:
        print(f"Error loading backup: {e}")
    
    return default_data

def validate_and_migrate_data(data):
    """Validate data structure and migrate from older versions if needed."""
    # Ensure required keys exist
    if "flashcards" not in data:
        data["flashcards"] = []
    
    if "stats" not in data:
        data["stats"] = {"correct": 0, "total": 0}
    
    if "settings" not in data:
        data["settings"] = {
            "default_time_limit": 10,
            "auto_save": True,
            "sound_enabled": True
        }
    
    if "version" not in data:
        data["version"] = "2.0"
    
    if "created" not in data:
        data["created"] = datetime.now().isoformat()
    
    # Update last modified time
    data["last_modified"] = datetime.now().isoformat()
    
    # Validate flashcards structure
    valid_flashcards = []
    for card in data["flashcards"]:
        if isinstance(card, dict) and "question" in card and "answer" in card:
            # Ensure question and answer are strings
            card["question"] = str(card["question"]).strip()
            card["answer"] = str(card["answer"]).strip()
            
            if card["question"] and card["answer"]:
                valid_flashcards.append(card)
    
    data["flashcards"] = valid_flashcards
    
    # Validate stats
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
        # Create backup before saving
        create_backup()
        
        # Update last modified time
        data["last_modified"] = datetime.now().isoformat()
        
        # Write to temporary file first to prevent corruption
        temp_file = DATA_FILE + ".tmp"
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        # Verify the temporary file is valid JSON
        with open(temp_file, 'r', encoding='utf-8') as f:
            json.load(f)  # This will raise an exception if the JSON is invalid
        
        # If verification passed, replace the original file
        shutil.move(temp_file, DATA_FILE)
        
    except Exception as e:
        # Clean up temporary file if it exists
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
        version = data.get("version", "1.0")
        
        info = f"""
Data File Information:
- File: {DATA_FILE}
- Version: {version}
- Flashcards: {flashcard_count}
- Total attempts: {stats.get('total', 0)}
- Correct answers: {stats.get('correct', 0)}
- Accuracy: {(stats.get('correct', 0) / max(stats.get('total', 1), 1) * 100):.1f}%
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
        
        # Validate imported data
        validated_data = validate_and_migrate_data(imported_data)
        
        # Save the imported data
        save_data(validated_data)
        
        return f"Data imported successfully from {import_path}"
    except Exception as e:
        return f"Error importing data: {e}"