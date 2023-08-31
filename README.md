# XML Data Extraction Script
This Python script extracts useful information from XML files of a specific format and outputs the names of items and their associated spare parts. The script is designed to work within a Docker environment and can be used to extract data from XML files provided in a zip archive.

## Demo
The script is currently deployed on `https://zmgq4lsekrshofijzmco4tflpi0xlece.lambda-url.eu-central-1.on.aws`
You can try open the following links:
- `https://zmgq4lsekrshofijzmco4tflpi0xlece.lambda-url.eu-central-1.on.aws/docs` - the documentation
- `https://zmgq4lsekrshofijzmco4tflpi0xlece.lambda-url.eu-central-1.on.aws/items/count` - the number of items in a sample zip file
- `https://zmgq4lsekrshofijzmco4tflpi0xlece.lambda-url.eu-central-1.on.aws/items/names` - the names of items
- `https://zmgq4lsekrshofijzmco4tflpi0xlece.lambda-url.eu-central-1.on.aws/items/parts` - the names of items and their spare parts

## Requirements
Docker and Docker Compose should be installed on your system.

## Setup

Clone the repository

```bash
git clone https://github.com/ozerodar/xml-products-extractor.git && cd xml-products-extractor
```

Build a docker image
```bash
docker-compose build
```

Start the server
```bash
docker-compose up
```
The Uvicorn server will run on: http://localhost:8000

## Usage

The script has three main functions:
- count `/items/count`: outputs the number of items in a .xml file
- names `/items/names`: outputs the names of items in a .xml file
- parts `/items/parts`: outputs the names of items and their spare parts (if present)

Each endpoint has an optional argument `url` that points to a zip file containing xml files. If `url` is not provided, a sample file will be processed.

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
The script extracts names of items and their associated spare parts (if applicable) and returns them in a request. The script is supposed to run in a browser, so the output string is an html string. For more information, see the documentation at `http://localhost:8000`.
