import os, platform

from pathlib import Path
from prompt_toolkit.styles import Style

DIR: Path = Path(__file__).parent
STORAGE_PATH: Path = DIR / "storage"
PLUGINS_PATH: Path = DIR / "plugins"
SYS_ROOT: str = os.path.abspath(os.sep)
EP_MODULE: str = str(DIR).removeprefix(SYS_ROOT).replace("\\", "/").replace("/", ".")
PLATFORM: str = platform.system().lower()
STYLE = Style.from_dict({
    'yellow': 'bold fg:yellow',
    'magenta': 'fg:magenta',
    'blue': 'bold fg:blue',
    'reset': '',
})
META_JSON_FRAME: str = """
{
    "cmd_history": [],
    "cd_history": [],
    "aliases": {},
    "props": {},
    "last_location": "",
    "cache": []
}
"""