from pathlib import Path

DIR_ZIP = Path('/tmp') / "data" / "zip"
DIR_XML = Path('/tmp') / "data" / "xml"

DIR_ZIP.mkdir(parents=True, exist_ok=True)
DIR_XML.mkdir(parents=True, exist_ok=True)
