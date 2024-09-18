from pydantic import BaseModel
from typing import Optional
from datetime import date

class Installation(BaseModel):
    """Installation model.

    Attributes:
        id (int): The unique identifier of the installation.
        name (str): The name of the installation.
        description (str): The description of the installation.
        product_id (int): The ID of the associated product.
        customer_id (int): The ID of the associated customer.
        installation_date (date): The date of the installation.
    """
    id: int
    name: str
    description: str
    product_id: int
    customer_id: int
    installation_date: date

class InstallationCreate(BaseModel):
    """Installation creation model.

    Attributes:
        id (int): The unique identifier of the installation.
        name (str): The name of the installation.
        description (str): The description of the installation.
        product_id (int): The ID of the associated product.
        customer_id (int): The ID of the associated customer.
        installation_date (date): The date of the installation.
    """
    id: int
    name: str
    description: str
    product_id: int
    customer_id: int
    installation_date: date

class InstallationUpdate(BaseModel):
    """Installation update model.

    Attributes:
        name (Optional[str]): The name of the installation.
        description (Optional[str]): The description of the installation.
        product_id (Optional[int]): The ID of the associated product.
        customer_id (Optional[int]): The ID of the associated customer.
        installation_date (Optional[date]): The date of the installation.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    product_id: Optional[int] = None
    customer_id: Optional[int] = None
    installation_date: Optional[date] = None