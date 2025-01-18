import json
import os
from pathlib import Path
from typing import Dict, Optional


class JsonStorage:
    def __init__(self, directory: str = "data/entries"):
        self.directory = Path(directory)
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        self.directory.mkdir(parents=True, exist_ok=True)

    def _get_entry_path(self, entry_id: str) -> Path:
        return self.directory / f"{entry_id}.json"

    def load_entry(self, entry_id: str) -> Optional[str]:
        try:
            with open(self._get_entry_path(entry_id), 'r') as f:
                return json.load(f)['content']
        except FileNotFoundError:
            return None

    def load_all(self) -> Dict[str, str]:
        entries = {}
        for file_path in self.directory.glob('*.json'):
            entry_id = file_path.stem
            with open(file_path, 'r') as f:
                entries[entry_id] = json.load(f)['content']
        return entries

    def save_entry(self, entry_id: str, content: str):
        with open(self._get_entry_path(entry_id), 'w') as f:
            json.dump({'content': content}, f, indent=2)

    def delete_entry(self, entry_id: str) -> bool:
        try:
            self._get_entry_path(entry_id).unlink()
            return True
        except FileNotFoundError:
            return False

    def purge(self):
        for file_path in self.directory.glob('*.json'):
            file_path.unlink()
