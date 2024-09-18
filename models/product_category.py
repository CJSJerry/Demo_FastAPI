from pydantic import BaseModel
from typing import Optional

class ProductCategory(BaseModel):
    """ProductCategory model.

    Attributes:
        id (int): The unique identifier of the product category.
        name (str): The name of the product category.
    """
    id: int
    name: str

class ProductCategoryCreate(BaseModel):
    """ProductCategory creation model.

    Attributes:
        id (int): The unique identifier of the product category.
        name (str): The name of the product category.
    """
    id: int
    name: str

class ProductCategoryUpdate(BaseModel):
    """ProductCategory update model.

    Attributes:
        name (Optional[str]): The name of the product category.
    """
    name: Optional[str] = None