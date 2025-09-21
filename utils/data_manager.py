import json
import os
from datetime import datetime
import pandas as pd

class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.mood_file = os.path.join(data_dir, "mood_data.json")
        self.profile_file = os.path.join(data_dir, "user_profiles.json")
        self.journal_file = os.path.join(data_dir, "journal_entries.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
    
    def save_mood_entry(self, user_id, mood_entry):
        """Save a mood entry to file"""
        data = self._load_json(self.mood_file)
        
        if user_id not in data:
            data[user_id] = []
        
        # Convert datetime to string for JSON serialization
        mood_entry['date'] = mood_entry['date'].isoformat() if isinstance(mood_entry['date'], datetime) else mood_entry['date']
        
        data[user_id].append(mood_entry)
        self._save_json(self.mood_file, data)
    
    def load_mood_history(self, user_id):
        """Load mood history for a user"""
        data = self._load_json(self.mood_file)
        user_data = data.get(user_id, [])
        
        # Convert date strings back to datetime objects
        for entry in user_data:
            if isinstance(entry['date'], str):
                entry['date'] = datetime.fromisoformat(entry['date'])
        
        return user_data
    
    def save_journal_entry(self, user_id, journal_entry):
        """Save a journal entry to file"""
        data = self._load_json(self.journal_file)
        
        if user_id not in data:
            data[user_id] = []
        
        # Convert datetime to string for JSON serialization
        journal_entry['date'] = journal_entry['date'].isoformat() if isinstance(journal_entry['date'], datetime) else journal_entry['date']
        
        data[user_id].append(journal_entry)
        self._save_json(self.journal_file, data)
    
    def load_journal_entries(self, user_id):
        """Load journal entries for a user"""
        data = self._load_json(self.journal_file)
        user_data = data.get(user_id, [])
        
        # Convert date strings back to datetime objects
        for entry in user_data:
            if isinstance(entry['date'], str):
                entry['date'] = datetime.fromisoformat(entry['date'])
        
        return user_data
    
    def save_user_profile(self, user_id, profile):
        """Save user profile"""
        data = self._load_json(self.profile_file)
        data[user_id] = profile
        self._save_json(self.profile_file, data)
    
    def load_user_profile(self, user_id):
        """Load user profile"""
        data = self._load_json(self.profile_file)
        return data.get(user_id, {
            'name': '',
            'age': 25,
            'preferences': []
        })
    
    def export_user_data(self, user_id):
        """Export all user data as CSV"""
        mood_data = self.load_mood_history(user_id)
        journal_data = self.load_journal_entries(user_id)
        
        if mood_data:
            mood_df = pd.DataFrame(mood_data)
            mood_csv = mood_df.to_csv(index=False)
        else:
            mood_csv = "No mood data available"
        
        if journal_data:
            journal_df = pd.DataFrame(journal_data)
            journal_csv = journal_df.to_csv(index=False)
        else:
            journal_csv = "No journal data available"
        
        return mood_csv, journal_csv
    
    def _load_json(self, filepath):
        """Load JSON data from file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_json(self, filepath, data):
        """Save data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)