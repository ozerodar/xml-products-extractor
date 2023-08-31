import requests
from zipfile import ZipFile
from pathlib import Path
from urllib.parse import urlparse

from app import DIR_XML, DIR_ZIP


def download_zip(url, path):
    """Downloads the zip file from the given url and saves it to the given path."""
    print("Downloading zip file...")
    try:
        response = requests.get(url)
        with path.open("wb") as zip_file:
            zip_file.write(response.content)
            if not path.exists():
                print("Downloaded zip file does not exist.")
    except Exception as e:
        print(f"Failed to download file: {e}")


def extract_zip(zip_path, target_path):
    """Extracts the zip file contents directly into the target directory."""
    if zip_path.exists():
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(target_path)


def download_and_extract_zip(url):
    url_path = urlparse(url).path
    filename = Path(url_path).name

    zip_path = DIR_ZIP / filename
    xml_path = DIR_XML / filename.replace(".zip", "")

    if not zip_path.exists():
        download_zip(url, zip_path)
    if not xml_path.exists():
        extract_zip(zip_path, xml_path)
    print("Download and extraction completed.")
    return xml_path
