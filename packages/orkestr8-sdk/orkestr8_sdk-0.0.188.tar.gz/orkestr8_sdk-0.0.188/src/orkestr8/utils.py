import os
from pathlib import Path


def create_file_if_not_exists(file_path: Path) -> None:
    """Wrapper to ensure `file_path` exists, even if empty"""
    if Path(file_path).exists():
        return
    os.makedirs(str(file_path.parent), exist_ok=True)
    with open(str(file_path), "w"):
        pass
