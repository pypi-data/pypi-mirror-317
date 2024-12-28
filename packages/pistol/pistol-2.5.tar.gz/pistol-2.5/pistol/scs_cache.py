from pathlib import Path

from .meta import MetaJSON
from .logging import info

class SCSCacheManager:
    def __init__(self, meta: MetaJSON):
        self.meta: MetaJSON = meta
        self.cache: list[tuple[Path, str]] = []
    def load(self):
        self.cache = [(Path(path), command) for (path, command) in self.meta.read()["cache"]]
    def save(self):
        self.meta.write(self.meta.read() | {"cache": [(str(path), command) for (path, command) in self.cache]})
    def clear(self):
        self.cache = []
    def suggest_commands(self, path: Path):
        suggestions: list[str] = []
        for cached_path, cached_command in self.cache:
            if str(path) == str(cached_path) or self.meta.fetch("scs-ignore-paths"):
                suggestions.append(cached_command)
        return list(set(suggestions))
    def remove_command(self, command: str, path: Path | None = None):
        new_cache: list[tuple[Path, str]] = []
        removed_commands: int = 0
        for cached_path, cached_command in self.cache:
            if (path is None or str(path) == str(cached_path)) and command == cached_command:
                removed_commands += 1
            else:
                new_cache.append((cached_path, cached_command))
        self.cache = new_cache
        info(f"removed {removed_commands} command{'s' if removed_commands != 1 else ''} matching {{command: '{command}', at: '{path or 'any'}'}}")
    def add(self, path: Path, command: str):
        self.cache = list(set(self.cache + [(path, command)]))