""" Data models to scrap catalog data """
# For doc info, see: https://docs.pydantic.dev/usage/models/

import datetime

from pydantic import BaseModel

class CatalogItem(BaseModel):
    """ Represents an item in a product catalog we monitor """
    id: str
    name: str                               # Name of the product
    price: float                              # Price of the product
    desc: str                               # Natural language description
    category: str | None                    # Item category. Free form string for now. Optional field
    specifications: dict[str, str] | None   # Key, value pairs with specifications. Optional field
    pictures: list[str]                     # Keep a list of file names with the item's pictures.
                                            # If none, it will be an empty list
    date: datetime.date                     # Date of scraping
