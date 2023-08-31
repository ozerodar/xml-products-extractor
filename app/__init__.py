from pathlib import Path

DIR_ZIP = Path(__file__).parent / "data" / "zip"
DIR_XML = Path(__file__).parent / "data" / "xml"

DIR_ZIP.mkdir(parents=True, exist_ok=True)
DIR_XML.mkdir(parents=True, exist_ok=True)
