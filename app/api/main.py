"""This module contains the API for the XML items xmlextractor."""
from functools import wraps
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse

from app.xmlextractor.extractor import get_items
from app.exceptions import ZipDownloadFailed, ZipExtractionFailed

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


def error_handler_async(func):
    """Decorator for handling errors in async functions"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except (ZipDownloadFailed, ZipExtractionFailed) as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    return wrapper


@app.get("/items/count", response_class=HTMLResponse, response_model=str)
@error_handler_async
async def list_item_count(url: str = DEFAULT_ZIP_URL) -> str:
    """API endpoint for counting items"""
    return HTML_TEMPLATE_COUNT.format(items=len(get_items(url=url)))


@app.get("/items/names", response_class=HTMLResponse, response_model=str)
@error_handler_async
async def list_item_names(url: str = DEFAULT_ZIP_URL) -> str:
    """API endpoint for listing item names"""
    names = "<br>".join([item.name for item in get_items(url=url)])
    return HTML_TEMPLATE_NAMES.format(names=names)


@app.get("/items/parts", response_class=HTMLResponse, response_model=str)
@error_handler_async
async def list_item_parts(url: str = DEFAULT_ZIP_URL) -> str:
    """API endpoint for listing item part names"""
    parts_rows = ""
    for item in get_items(url=url):
        parts = "".join([HTML_TEMPLATE_PART.format(part=part) for part in item.spare_parts])
        parts_list = HTML_TEMPLATE_PARTS_LIST.format(parts=parts) if parts else ""
        parts_rows += HTML_TEMPLATE_PARTS_ROW.format(name=item.name, parts_list=parts_list)

    return HTML_TEMPLATE_PARTS.format(parts_rows=parts_rows)
