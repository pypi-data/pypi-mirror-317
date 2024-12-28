import json

from pathlib import Path

from .constants import META_JSON_FRAME
from .prop_state import PropState


class MetaJSON:
    def __init__(self, path: Path):
        self.path: Path = path
    def create(self):
        if not self.path.exists():
            with self.path.open("w", encoding="utf-8") as file:
                file.write(META_JSON_FRAME)
    def write(self, data: dict):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4) # NOQA
    def read(self):
        if not self.path.exists():
            raise FileNotFoundError(f"The file {self.path} does not exist.")
        with self.path.open(encoding="utf-8") as file:
            return json.load(file)
    def fetch(self, key: str, default: PropState | None = None):
        return PropState(self.read()["props"].get(key, default or PropState(True)))