from pydantic import BaseModel
from typing import Optional

class Country(BaseModel):
    """Country model.

    Attributes:
        id (int): The unique identifier of the country.
        name (str): The name of the country.
        region (str): The region of the country.
    """
    id: int
    name: str
    region: str

class CountryCreate(BaseModel):
    """Country creation model.

    Attributes:
        id (int): The unique identifier of the country.
        name (str): The name of the country.
        region (str): The region of the country.
    """
    id: int
    name: str
    region: str

class CountryUpdate(BaseModel):
    """Country update model.

    Attributes:
        name (Optional[str]): The name of the country.
        region (Optional[str]): The region of the country.
    """
    name: Optional[str] = None
    region: Optional[str] = None