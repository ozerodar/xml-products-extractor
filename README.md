# XML Data Extraction Script
This Python script extracts useful information from XML files of a specific format and outputs the names of items and their associated spare parts. The script is designed to work within a Docker environment and can be used to extract data from XML files provided in a zip archive.

## Requirements
Docker and Docker Compose should be installed on your system.

## Usage

Clone the repository

```bash
git clone https://github.com/ozerodar/xml-products-extractor.git && cd xml-products-extractor
```

Build a docker image
```bash
docker-compose build
```

Run the script with the provided URL to the zip file containing XML data:

```bash
docker-compose run --rm app sh -c "python main.py [URL] [-v|--verbose]"
```
Replace [URL] with the actual URL of the zip file you want to process. Use the -v or --verbose flag to enable verbose logging to the screen, for example:

```bash
docker-compose run --rm app sh -c "python main.py https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip"
```

## Tests
You can run tests using the following command:

```bash
docker-compose run --rm app sh -c "pytest ../tests"
```

## XML Format
The script is designed to process XML files following a specific format. The XML file should contain a structure similar to:

```xml
<?xml version="1.0" encoding="utf-8"?>
<export_full>
    <items>
        <item name="Item 1"/>
        <item name="Item 2"/>
        <item name="Item 3">
            <parts>
                <part categoryId="6" name="Some other parts">
                    <item name="Part 1" />
                </part>
            </parts>
        </item>
        <item name="Item 4">
        <parts>
            <part categoryId="1" name="Spare parts">
                <item name="Part 1" />
                <item name="Part 2" />
            </part>
        </parts>
        </item>
    </items>
    <partCategories>
        <partCategory name="Spare parts" />
        <partCategory name="Some other parts" />
    </partCategories>
</export_full>
```
The script extracts information from the `<item>` and `<part>` elements within the XML data.

## Output
The script extracts names of items and their associated spare parts (if applicable) and either writes the output to a specified output file or logs it to the screen based on the provided command-line options.
