import json
import os
from pathlib import Path
from typing import Dict, Optional


class JsonStorage:
    def __init__(self, file_path: str = "data/journal_entries.json"):
        self.file_path = Path(file_path)
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.save({})

    def load(self) -> Dict:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save(self, data: Dict):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
