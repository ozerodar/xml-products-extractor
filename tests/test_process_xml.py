from app.xmlextractor.extractor import get_items_and_spare_parts_from_xml_file
from tests import DIR_TEST_FILE


def test_extract_items_no_file():
    items = get_items_and_spare_parts_from_xml_file("file_not_found.xml")
    assert items == []


def test_extract_items_empty_file():
    items = get_items_and_spare_parts_from_xml_file("empty.xml")
    assert items == []


def test_extract_items_names():
    items = get_items_and_spare_parts_from_xml_file(DIR_TEST_FILE)
    assert [item.model_dump() for item in items] == [
        {"name": "Item 1", "spare_parts": []},
        {"name": "Item 2", "spare_parts": []},
        {"name": "Item 3", "spare_parts": []},
        {"name": "Item 4", "spare_parts": ["Part 1", "Part 2"]},
    ]
