from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    """Product model.

    Attributes:
        id (int): The unique identifier of the product.
        reference (str): The reference code of the product.
        name (str): The name of the product.
        category_id (int): The ID of the product category.
        price (str): The price of the product.
    """
    id: int
    reference: str
    name: str
    category_id: int
    price: str

class ProductCreate(BaseModel):
    """Product creation model.

    Attributes:
        id (int): The unique identifier of the product.
        reference (str): The reference code of the product.
        name (str): The name of the product.
        category_id (int): The ID of the product category.
        price (str): The price of the product.
    """
    id: int
    reference: str
    name: str
    category_id: int
    price: str

class ProductUpdate(BaseModel):
    """Product update model.

    Attributes:
        reference (Optional[str]): The reference code of the product.
        name (Optional[str]): The name of the product.
        category_id (Optional[int]): The ID of the product category.
        price (Optional[str]): The price of the product.
    """
    reference: Optional[str] = None
    name: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[str] = None