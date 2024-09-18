from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.customer import Customer, CustomerCreate, CustomerUpdate
from dependencies import get_db
from crud.customer import CustomerCRUD

router = APIRouter()

def get_customer_crud(db=Depends(get_db)) -> CustomerCRUD:
    """Get a CustomerCRUD instance.

    Args:
        db (Optional[Depends]): Optional database dependency.

    Returns:
        CustomerCRUD: An instance of CustomerCRUD.
    """
    return CustomerCRUD(db)

@router.post("/customers/", response_model=Customer, status_code=201, responses={
    201: {"description": "Customer successfully created"},
    409: {"description": "Customer with this ID already exists"}})
async def create_customer(customer: CustomerCreate, crud: CustomerCRUD = Depends(get_customer_crud)) -> Customer:
    """Create a new customer.

    Args:
        customer (CustomerCreate): The customer data to create.
        crud (CustomerCRUD, optional): The CRUD instance. Defaults to Depends(get_customer_crud).

    Raises:
        HTTPException: If a customer with the given ID already exists.

    Returns:
        Customer: The created customer.
    """
    new_customer = await crud.create_customer(customer)
    if new_customer is None:
        raise HTTPException(status_code=409, detail=f"Customer with id {customer.id} already exists.")
    return new_customer

@router.get("/customers/", response_model=List[Customer])
async def read_customers(crud: CustomerCRUD = Depends(get_customer_crud)) -> List[Customer]:
    """Get a list of all customers.

    Args:
        crud (CustomerCRUD, optional): The CRUD instance. Defaults to Depends(get_customer_crud).

    Returns:
        List[Customer]: A list of all customers.
    """
    return await crud.get_customers()

@router.get("/customers/{customer_id}", response_model=Customer, responses={
    404: {"description": "Customer not found"}})
async def read_customer(customer_id: int, crud: CustomerCRUD = Depends(get_customer_crud)) -> Customer:
    """Get a customer by its ID.

    Args:
        customer_id (int): The ID of the customer to retrieve.
        crud (CustomerCRUD, optional): The CRUD instance. Defaults to Depends(get_customer_crud).

    Raises:
        HTTPException: If the customer with the given ID is not found.

    Returns:
        Customer: The customer with the given ID.
    """
    customer = await crud.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/customers/{customer_id}", status_code=204, responses={
    204: {"description": "Customer successfully deleted"},
    404: {"description": "Customer not found"}})
async def delete_customer(customer_id: int, crud: CustomerCRUD = Depends(get_customer_crud)) -> None:
    """Delete a customer by its ID.

    Args:
        customer_id (int): The ID of the customer to delete.
        crud (CustomerCRUD, optional): The CRUD instance. Defaults to Depends(get_customer_crud).

    Raises:
        HTTPException: If the customer with the given ID is not found.

    Returns:
        None: Indicates successful deletion.
    """
    customer = await crud.delete_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None

@router.put("/customers/{customer_id}", response_model=Customer, responses={
    200: {"description": "Customer successfully updated"}, 
    404: {"description": "Customer not found"}})
async def update_customer(customer_id: int, customer: CustomerCreate, crud: CustomerCRUD = Depends(get_customer_crud)) -> Customer:
    """Update a customer by its ID.

    Args:
        customer_id (int): The ID of the customer to update.
        customer (CustomerCreate): The new data for the customer.
        crud (CustomerCRUD, optional): The CRUD instance. Defaults to Depends(get_customer_crud).

    Raises:
        HTTPException: If the customer with the given ID is not found.

    Returns:
        Customer: The updated customer.
    """
    updated_customer = await crud.update_customer(customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer

@router.patch("/customers/{customer_id}", response_model=Customer, responses={
    200: {"description": "Customer successfully partially updated"}, 
    404: {"description": "Customer not found"}})
async def partial_update_customer(customer_id: int, customer: CustomerUpdate, crud: CustomerCRUD = Depends(get_customer_crud)) -> Customer:
    """Partially update a customer by its ID.

    Args:
        customer_id (int): The ID of the customer to update.
        customer (CustomerUpdate): The partial data for the customer.
        crud (CustomerCRUD, optional): The CRUD instance. Defaults to Depends(get_customer_crud).

    Raises:
        HTTPException: If the customer with the given ID is not found.

    Returns:
        Customer: The updated customer.
    """
    updated_customer = await crud.partial_update_customer(customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer