import subprocess

from .logging import error

def subprocess_run(command: list[str], solo_mode: str):
    try:
        subprocess.run(command)
    except Exception as exc:
        error(f"{solo_mode}: {exc}")