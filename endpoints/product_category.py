from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.product_category import ProductCategory, ProductCategoryCreate, ProductCategoryUpdate
from dependencies import get_db
from crud.product_category import ProductCategoryCRUD

router = APIRouter()

def get_product_category_crud(db=Depends(get_db)) -> ProductCategoryCRUD:
    """Get a ProductCategoryCRUD instance.

    Args:
        db (Optional[Depends]): Optional database dependency.

    Returns:
        ProductCategoryCRUD: An instance of ProductCategoryCRUD.
    """
    return ProductCategoryCRUD(db)

@router.post("/product_categories/", response_model=ProductCategory, status_code=201, responses={
    201: {"description": "Product category successfully created"},
    409: {"description": "Product category with this ID already exists"}})
async def create_product_category(category: ProductCategoryCreate, crud: ProductCategoryCRUD = Depends(get_product_category_crud)) -> ProductCategory:
    """Create a new product category.

    Args:
        category (ProductCategoryCreate): The product category data to create.
        crud (ProductCategoryCRUD, optional): The CRUD instance. Defaults to Depends(get_product_category_crud).

    Raises:
        HTTPException: If a product category with the given ID already exists.

    Returns:
        ProductCategory: The created product category.
    """
    new_category = await crud.create_product_category(category)
    if new_category is None:
        raise HTTPException(status_code=409, detail=f"Product category with id {category.id} already exists.")
    return new_category

@router.get("/product_categories/", response_model=List[ProductCategory])
async def read_product_categories(crud: ProductCategoryCRUD = Depends(get_product_category_crud)) -> List[ProductCategory]:
    """Get a list of all product categories.

    Args:
        crud (ProductCategoryCRUD, optional): The CRUD instance. Defaults to Depends(get_product_category_crud).

    Returns:
        List[ProductCategory]: A list of all product categories.
    """
    return await crud.get_product_categories()

@router.get("/product_categories/{category_id}", response_model=ProductCategory, responses={
    404: {"description": "Product category not found"}})
async def read_product_category(category_id: int, crud: ProductCategoryCRUD = Depends(get_product_category_crud)) -> ProductCategory:
    """Get a product category by its ID.

    Args:
        category_id (int): The ID of the product category to retrieve.
        crud (ProductCategoryCRUD, optional): The CRUD instance. Defaults to Depends(get_product_category_crud).

    Raises:
        HTTPException: If the product category with the given ID is not found.

    Returns:
        ProductCategory: The product category with the given ID.
    """
    category = await crud.get_product_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Product category not found")
    return category

@router.delete("/product_categories/{category_id}", status_code=204, responses={
    204: {"description": "Product category successfully deleted"},
    404: {"description": "Product category not found"}})
async def delete_product_category(category_id: int, crud: ProductCategoryCRUD = Depends(get_product_category_crud)) -> None:
    """Delete a product category by its ID.

    Args:
        category_id (int): The ID of the product category to delete.
        crud (ProductCategoryCRUD, optional): The CRUD instance. Defaults to Depends(get_product_category_crud).

    Raises:
        HTTPException: If the product category with the given ID is not found.

    Returns:
        None: Indicates successful deletion.
    """
    category = await crud.delete_product_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Product category not found")
    return None

@router.put("/product_categories/{category_id}", response_model=ProductCategory, responses={
    200: {"description": "Product category successfully updated"}, 
    404: {"description": "Product category not found"}})
async def update_product_category(category_id: int, category: ProductCategoryCreate, crud: ProductCategoryCRUD = Depends(get_product_category_crud)) -> ProductCategory:
    """Update a product category by its ID.

    Args:
        category_id (int): The ID of the product category to update.
        category (ProductCategoryCreate): The new data for the product category.
        crud (ProductCategoryCRUD, optional): The CRUD instance. Defaults to Depends(get_product_category_crud).

    Raises:
        HTTPException: If the product category with the given ID is not found.

    Returns:
        ProductCategory: The updated product category.
    """
    updated_category = await crud.update_product_category(category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Product category not found")
    return updated_category

@router.patch("/product_categories/{category_id}", response_model=ProductCategory, responses={
    200: {"description": "Product category successfully partially updated"}, 
    404: {"description": "Product category not found"}})
async def partial_update_product_category(category_id: int, category: ProductCategoryUpdate, crud: ProductCategoryCRUD = Depends(get_product_category_crud)) -> ProductCategory:
    """Partially update a product category by its ID.

    Args:
        category_id (int): The ID of the product category to update.
        category (ProductCategoryUpdate): The partial data for the product category.
        crud (ProductCategoryCRUD, optional): The CRUD instance. Defaults to Depends(get_product_category_crud).

    Raises:
        HTTPException: If the product category with the given ID is not found.

    Returns:
        ProductCategory: The updated product category.
    """
    updated_category = await crud.partial_update_product_category(category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Product category not found")
    return updated_category
