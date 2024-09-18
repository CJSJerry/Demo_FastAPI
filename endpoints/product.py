from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.product import Product, ProductCreate, ProductUpdate
from dependencies import get_db
from crud.product import ProductCRUD

router = APIRouter()

def get_product_crud(db=Depends(get_db)) -> ProductCRUD:
    """Get a ProductCRUD instance.

    Args:
        db (Optional[Depends]): Optional database dependency.

    Returns:
        ProductCRUD: An instance of ProductCRUD.
    """
    return ProductCRUD(db)

@router.post("/products/", response_model=Product, status_code=201, responses={
    201: {"description": "Product successfully created"},
    409: {"description": "Product with this ID already exists"}})
async def create_product(product: ProductCreate, crud: ProductCRUD = Depends(get_product_crud)) -> Product:
    """Create a new product.

    Args:
        product (ProductCreate): The product data to create.
        crud (ProductCRUD, optional): The CRUD instance. Defaults to Depends(get_product_crud).

    Raises:
        HTTPException: If a product with the given ID already exists.

    Returns:
        Product: The created product.
    """
    new_product = await crud.create_product(product)
    if new_product is None:
        raise HTTPException(status_code=409, detail=f"Product with id {product.id} already exists.")
    return new_product

@router.get("/products/", response_model=List[Product])
async def read_products(crud: ProductCRUD = Depends(get_product_crud)) -> List[Product]:
    """Get a list of all products.

    Args:
        crud (ProductCRUD, optional): The CRUD instance. Defaults to Depends(get_product_crud).

    Returns:
        List[Product]: A list of all products.
    """
    return await crud.get_products()

@router.get("/products/{product_id}", response_model=Product, responses={
    404: {"description": "Product not found"}})
async def read_product(product_id: int, crud: ProductCRUD = Depends(get_product_crud)) -> Product:
    """Get a product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.
        crud (ProductCRUD, optional): The CRUD instance. Defaults to Depends(get_product_crud).

    Raises:
        HTTPException: If the product with the given ID is not found.

    Returns:
        Product: The product with the given ID.
    """
    product = await crud.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/products/{product_id}", status_code=204, responses={
    204: {"description": "Product successfully deleted"},
    404: {"description": "Product not found"}})
async def delete_product(product_id: int, crud: ProductCRUD = Depends(get_product_crud)) -> None:
    """Delete a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.
        crud (ProductCRUD, optional): The CRUD instance. Defaults to Depends(get_product_crud).

    Raises:
        HTTPException: If the product with the given ID is not found.

    Returns:
        None: Indicates successful deletion.
    """
    product = await crud.delete_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return None

@router.put("/products/{product_id}", response_model=Product, responses={
    200: {"description": "Product successfully updated"}, 
    404: {"description": "Product not found"}})
async def update_product(product_id: int, product: ProductCreate, crud: ProductCRUD = Depends(get_product_crud)) -> Product:
    """Update a product by its ID.

    Args:
        product_id (int): The ID of the product to update.
        product (ProductCreate): The new data for the product.
        crud (ProductCRUD, optional): The CRUD instance. Defaults to Depends(get_product_crud).

    Raises:
        HTTPException: If the product with the given ID is not found.

    Returns:
        Product: The updated product.
    """
    updated_product = await crud.update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.patch("/products/{product_id}", response_model=Product, responses={
    200: {"description": "Product successfully partially updated"}, 
    404: {"description": "Product not found"}})
async def partial_update_product(product_id: int, product: ProductUpdate, crud: ProductCRUD = Depends(get_product_crud)) -> Product:
    """Partially update a product by its ID.

    Args:
        product_id (int): The ID of the product to update.
        product (ProductUpdate): The partial data for the product.
        crud (ProductCRUD, optional): The CRUD instance. Defaults to Depends(get_product_crud).

    Raises:
        HTTPException: If the product with the given ID is not found.

    Returns:
        Product: The updated product.
    """
    updated_product = await crud.partial_update_product(product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product