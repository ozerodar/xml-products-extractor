import argparse

from pathlib import Path

from file_manager import download_and_extract_zip
from extractor import get_items_and_spare_parts_from_xml_file
from utils import format_items, write_output_to_file

DIR_OUTPUT = Path("data/output")
DIR_OUTPUT.mkdir(parents=True, exist_ok=True)


def main(url: str, verbose: bool = False):
    path = download_and_extract_zip(url)
    for file in list(Path(path).glob("*.xml")):
        items = get_items_and_spare_parts_from_xml_file(str(file))
        formatted_items = format_items(items)
        output_file = DIR_OUTPUT / f"{file.stem}.txt"
        write_output_to_file(output_file, formatted_items)
        print(f"Result of extraction is saved to {output_file}. Number of items in the file: {len(items)}.")
        if verbose:
            print(formatted_items)


parser = argparse.ArgumentParser(description="The script extracts data from xml files and saves it to txt files")
parser.add_argument("url", help="The url of the xml file")
parser.add_argument("-v", "--verbose", default=False, required=False, help="Prints the progress", action="store_true")
url, verbose = vars(parser.parse_args()).values()

# example of usage "python3 main.py https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip --v"
main(url, verbose)
