#!/usr/bin/env python3
"""
Data storage module for Monkey-CLI.
Handles persistence of typing test results and historical data.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class DataStorage:
    """Manages storage and retrieval of typing test results."""
    
    def __init__(self, data_file: Optional[str] = None):
        """
        Initialize data storage.
        
        Args:
            data_file: Path to the data file. If None, uses default location.
        """
        if data_file is None:
            # Use user's home directory
            home = Path.home()
            data_dir = home / ".monkey-cli"
            data_dir.mkdir(exist_ok=True)
            self.data_file = data_dir / "history.json"
        else:
            self.data_file = Path(data_file)
        
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the data file exists."""
        if not self.data_file.exists():
            self._save_data([])
    
    def _load_data(self) -> List[Dict]:
        """Load data from file."""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Dict]):
        """Save data to file."""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_result(self, wpm: float, accuracy: float, 
                   correct_chars: int, incorrect_chars: int, 
                   total_chars: int, duration: int):
        """
        Save a typing test result.
        
        Args:
            wpm: Words per minute
            accuracy: Accuracy percentage
            correct_chars: Number of correct characters
            incorrect_chars: Number of incorrect characters
            total_chars: Total characters typed
            duration: Test duration in seconds
        """
        data = self._load_data()
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "wpm": round(wpm, 2),
            "accuracy": round(accuracy, 2),
            "correct_chars": correct_chars,
            "incorrect_chars": incorrect_chars,
            "total_chars": total_chars,
            "duration": duration
        }
        
        data.append(result)
        
        # Keep only last 100 results to avoid file bloat
        if len(data) > 100:
            data = data[-100:]
        
        self._save_data(data)
    
    def get_all_results(self) -> List[Dict]:
        """Get all stored results."""
        return self._load_data()
    
    def get_recent_results(self, count: int = 10) -> List[Dict]:
        """Get the most recent N results."""
        data = self._load_data()
        return data[-count:] if len(data) >= count else data
    
    def get_statistics(self) -> Dict:
        """
        Get overall statistics.
        
        Returns:
            Dict with average WPM, accuracy, best WPM, total tests, etc.
        """
        data = self._load_data()
        
        if not data:
            return {
                "total_tests": 0,
                "average_wpm": 0.0,
                "average_accuracy": 0.0,
                "best_wpm": 0.0,
                "best_accuracy": 0.0,
                "total_chars": 0
            }
        
        wpms = [r["wpm"] for r in data]
        accuracies = [r["accuracy"] for r in data]
        
        return {
            "total_tests": len(data),
            "average_wpm": round(sum(wpms) / len(wpms), 2),
            "average_accuracy": round(sum(accuracies) / len(accuracies), 2),
            "best_wpm": round(max(wpms), 2),
            "best_accuracy": round(max(accuracies), 2),
            "total_chars": sum(r["total_chars"] for r in data)
        }
    
    def clear_history(self):
        """Clear all stored results."""
        self._save_data([])
