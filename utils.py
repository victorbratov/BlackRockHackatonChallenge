import os.path
from typing import Optional


def get_page(page_name: str, directory: str) -> Optional[str]:
    try:
        content = ""
        if os.path.exists(f"{directory}/{page_name}.txt"):
            with open(f"{directory}/{page_name}.txt", "r") as file:
                content += file.read()
            return content
        else:
            return None
    except OSError as e:
        print(f"Error: Failed to open/read file {directory}/{page_name}.txt: {e}")
        return None
