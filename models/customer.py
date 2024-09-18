from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    """Customer model.

    Attributes:
        id (int): The unique identifier of the customer.
        name (str): The name of the customer.
        email (str): The email address of the customer.
        country_id (int): The ID of the country where the customer is located.
        premium_customer (str): Indicates if the customer is a premium customer.
    """
    id: int
    name: str
    email: str
    country_id: int
    premium_customer: str

class CustomerCreate(BaseModel):
    """Customer creation model.

    Attributes:
        id (int): The unique identifier of the customer.
        name (str): The name of the customer.
        email (str): The email address of the customer.
        country_id (int): The ID of the country where the customer is located.
        premium_customer (str): Indicates if the customer is a premium customer.
    """
    id: int
    name: str
    email: str
    country_id: int
    premium_customer: str

class CustomerUpdate(BaseModel):
    """Customer update model.

    Attributes:
        name (Optional[str]): The name of the customer.
        email (Optional[str]): The email address of the customer.
        country_id (Optional[int]): The ID of the country where the customer is located.
        premium_customer (Optional[str]): Indicates if the customer is a premium customer.
    """
    name: Optional[str] = None
    email: Optional[str] = None
    country_id: Optional[int] = None
    premium_customer: Optional[str] = None