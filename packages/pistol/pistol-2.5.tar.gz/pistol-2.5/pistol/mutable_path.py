import os

from pathlib import Path

from .constants import STORAGE_PATH
from .logging import warning, info, error, hint

class MutablePath:
    def __init__(self, path: Path | None = None):
        self.root: str = os.path.abspath(os.sep)
        self.path: Path = path or Path(self.root)
        self.set(str(self.path), [])
    def set(self, path: str, cd_history: list[str], ucd: bool = False, st: bool = False):
        old_path = self.path
        if str(self.path) == str(STORAGE_PATH) and not (ucd or st):
            warning("cannot use cd in storage mode, use st to exit storage mode first.")
            return
        if path == "..":
            self.path = self.path.parent
        elif path == ".":
            ...
        else:
            self.path /= path
        if not self.path.exists() and st:
            warning("storage directory does not exist, creating now.")
            os.mkdir(str(self.path))
            info("storage directory created successfully")
        if not self.path.exists() or not self.path.is_dir():
            error(f"{self.path} is not a valid path.")
            self.path = old_path
        else:
            cd_history.append(str(old_path))
        if self.path == str(STORAGE_PATH) and not st:
            hint("use the st command to switch to storage mode easier")