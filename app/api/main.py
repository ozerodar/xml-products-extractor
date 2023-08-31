"""This module contains the API for the XML items xmlextractor."""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.xmlextractor.extractor import get_items

app = FastAPI(title="XML items xmlextractor")

DEFAULT_ZIP_URL = "https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip"
HTML_TEMPLATE_COUNT = f"""
    <html>
        <head>
            <title>Number of items</title>
        </head>
        <body>
            <h1>Number of items: {{items}}</h1>
        </body>
    </html>
    """

HTML_TEMPLATE_NAMES = f"""
    <html>
        <head>
            <title>Item names</title>
        </head>
        <body>
            <p>{{names}}</p>
        </body>
    </html>
    """

HTML_TEMPLATE_PART = f"<li>{{part}}</li>"
HTML_TEMPLATE_PARTS_LIST = f"""<ul>{{parts}}</ul>"""
HTML_TEMPLATE_PARTS_ROW = f"""
                <tr>
                    <td>{{name}}</td>
                    <td>
                        {{parts_list}}
                    </td>
                </tr>
            """
HTML_TABLE_STYLE = """
            <style>
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }}
            </style>
            """

HTML_TEMPLATE_PARTS = f"""
    <html>
        <head>
            {HTML_TABLE_STYLE}
        </head>
        <body>
            <h2>Items and Spare Parts</h2>
            <table>
                <tr>
                    <th>Item Name</th>
                    <th>Spare Parts</th>
                </tr>
                {{parts_rows}}
            </table>
        </body>
    </html>
"""



@app.get("/items/count", response_class=HTMLResponse)
async def list_item_count(url: str = DEFAULT_ZIP_URL) -> str:
    """API endpoint for counting items"""
    return HTML_TEMPLATE_COUNT.format(items=len(get_items(url=url)))


@app.get("/items/names", response_class=HTMLResponse)
async def list_item_names(url: str = DEFAULT_ZIP_URL) -> str:
    names = "<br>".join([item.name for item in get_items(url=url)])
    return HTML_TEMPLATE_NAMES.format(names=names)


@app.get("/items/parts", response_class=HTMLResponse)
async def list_item_parts(url: str = DEFAULT_ZIP_URL) -> str:
    parts_rows = ""
    for item in get_items(url=url):
        parts = "".join([HTML_TEMPLATE_PART.format(part=part) for part in item.spare_parts])
        parts_list = HTML_TEMPLATE_PARTS_LIST.format(parts=parts) if parts else ""
        parts_rows += HTML_TEMPLATE_PARTS_ROW.format(name=item.name, parts_list=parts_list)

    return HTML_TEMPLATE_PARTS.format(parts_rows=parts_rows)
