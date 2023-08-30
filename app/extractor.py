import xml.etree.ElementTree as ET
from pathlib import Path

QUERY_SPARE_PARTS = "./parts/part/[@categoryId='1']."

def get_items_and_spare_parts_from_xml_file(xml_path):
    """
    This function gets the items and spare parts from the XML file.
    """
    items = []
    if Path(xml_path).exists():
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for item in root.findall("./items/item"):
            spare_parts = [sp.attrib.get('name') for parts in item.findall(QUERY_SPARE_PARTS) for sp in parts]
            items.append({"name": item.attrib.get("name"), "spare_parts": spare_parts})
    else:
        print(f"File {xml_path} does not exist.")
    return items
