import json
import os
from typing import List, Dict, Any
from datetime import datetime

class StatsManager:
    def __init__(self, stats_dir: str = "stats"):
        self.stats_dir = stats_dir
        os.makedirs(self.stats_dir, exist_ok=True)
        self.stats_file = os.path.join(self.stats_dir, "typing_stats.json")

    def save_session(self, wpm: int, accuracy: int, mode: str) -> None:
        stats = self.load_all_stats()
        session = {
            "date": datetime.now().isoformat(),
            "wpm": wpm,
            "accuracy": accuracy,
            "mode": mode
        }
        stats["sessions"].append(session)

        if wpm > stats["best_wpm"]:
            stats["best_wpm"] = wpm
        if accuracy > stats["best_accuracy"]:
            stats["best_accuracy"] = accuracy

        with open(self.stats_file, 'w') as f:
            json.dump(stats, f, indent=2)

    def load_all_stats(self) -> Dict[str, Any]:
        if not os.path.exists(self.stats_file):
            return {
                "best_wpm": 0,
                "best_accuracy": 0,
                "sessions": []
            }
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {
                "best_wpm": 0,
                "best_accuracy": 0,
                "sessions": []
            }

    def get_best_stats(self) -> tuple:
        stats = self.load_all_stats()
        return stats["best_wpm"], stats["best_accuracy"]
