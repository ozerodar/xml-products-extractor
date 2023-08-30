"""Utils file for the project."""
from typing import Dict, List
from pathlib import Path

DIR_OUTPUT = Path('app/data/output')
DIR_OUTPUT.mkdir(parents=True, exist_ok=True)

def format_items(items: List[Dict[str, str | List[str]]]) -> str:
    """Formats the items."""
    return f"Number of items: {len(items)}\n" + "\n".join([f"{item['name']}, spare parts: [{', '.join(item['spare_parts'])}]" if item['spare_parts'] else item['name'] for item in items])


def write_output_to_file(output_file: Path, content: str) -> None:
    """Writes the content to the file."""
    with output_file.open("w", encoding ="utf-8") as f:
        f.write(content)
