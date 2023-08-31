"""This module is responsible for extracting the items and spare parts from the XML file."""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

import app.models.m_internal as mi
from app.xmlextractor.file_manager import download_and_extract_zip


QUERY_SPARE_PARTS = "./parts/part/[@categoryId='1']."


def get_items_and_spare_parts_from_xml_file(xml_path: str) -> List[mi.Item]:
    """This function gets the items and spare parts from the XML file."""
    items = []
    if Path(xml_path).exists():
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for item in root.findall("./items/item"):
            spare_parts = [sp.attrib.get("name") for parts in item.findall(QUERY_SPARE_PARTS) for sp in parts]
            items.append(mi.Item(name=item.attrib.get("name"), spare_parts=spare_parts))
    return items


def get_items(url: str) -> List[mi.Item]:
    """This function downloads zip, extracts it and returns the items from all xml files it can find"""
    path = download_and_extract_zip(url)
    items = []
    for file in list(Path(path).glob("*.xml")):  # find all xml files in zip
        items.extend(get_items_and_spare_parts_from_xml_file(str(file)))
    return items
