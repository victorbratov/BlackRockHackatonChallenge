import os.path
import time
from typing import Optional


def get_help_page(page_name: str) -> Optional[str]:
    try:
        content = ""
        if os.path.exists(f"help/{page_name}.txt"):
            with open(f"help/{page_name}.txt", "r") as file:
                content += file.read().replace('\n', '')
            return content
        else:
            return None
    except OSError as e:
        print(f"Error: Failed to open/read file help/{page_name}.txt: {e}")
        return None


def get_current_month() -> int:
    return int(time.strftime("%m"))
