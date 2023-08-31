"""This module contains the functions for downloading and extracting zip files."""
import requests
from zipfile import ZipFile
from pathlib import Path
from urllib.parse import urlparse

from app import DIR_XML, DIR_ZIP
from app.exceptions import ZipDownloadFailed, ZipExtractionFailed


def download_zip(url: str, path: Path) -> None:
    """Downloads the zip file from the given url and saves it to the given path."""
    try:
        response = requests.get(url)
        with path.open("wb") as zip_file:
            zip_file.write(response.content)
            if not path.exists():
                raise ZipDownloadFailed("Failed to save zip file")
    except Exception as e:
        raise ZipDownloadFailed(f"Failed to download file: {e}") from e


def extract_zip(zip_path: str, target_path: str) -> None:
    """Extracts the zip file contents directly into the target directory."""
    if zip_path.exists():
        try:
            with ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(target_path)
        except Exception as e:
            raise ZipExtractionFailed(f"Failed to extract zip file: {e}") from e


def download_and_extract_zip(url: str) -> str:
    """Downloads and extracts the zip file from the given url.
    Returns the path to the extracted xml file.
    """
    url_path = urlparse(url).path
    filename = Path(url_path).name

    zip_path = DIR_ZIP / filename
    xml_path = DIR_XML / filename.replace(".zip", "")

    if not zip_path.exists():
        download_zip(url, zip_path)
    if not xml_path.exists():
        extract_zip(zip_path, xml_path)
    return xml_path
