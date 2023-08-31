"""Models for the items (internal use only) """
from pydantic import BaseModel


class Item(BaseModel):
    name: str = ""
    spare_parts: list = []
