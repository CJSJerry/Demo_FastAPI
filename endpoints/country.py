from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.country import Country, CountryCreate, CountryUpdate
from dependencies import get_db
from crud.country import CountryCRUD

# Connect to other files for this app
router = APIRouter()

# Initiate CountryCRUD instance with specified db dependency
def get_country_crud(db=Depends(get_db)) -> CountryCRUD:
    """Get a CountryCRUD instance.

    Args:
        db (Depends): Database dependency.

    Returns:
        CountryCRUD: An instance of CountryCRUD.
    """
    return CountryCRUD(db)

# FastAPI Endpoints
@router.post("/countries/", response_model=Country, status_code=201, responses={
    201: {"description": "Country successfully created"},
    409: {"description": "Country with this ID already exists"}})
async def create_country(country: CountryCreate, crud: CountryCRUD = Depends(get_country_crud)) -> Country:
    """Create a new country.

    Args:
        country (CountryCreate): The country data to create.
        crud (CountryCRUD, optional): The CRUD instance. Defaults to Depends(get_country_crud).

    Raises:
        HTTPException: If a country with the given ID already exists.

    Returns:
        Country: The created country.
    """
    new_country = await crud.create_country(country)
    if new_country is None:
        raise HTTPException(status_code=409, detail=f"Country with id {country.id} already exists.")
    return new_country

@router.get("/countries/", response_model=List[Country])
async def read_countries(crud: CountryCRUD = Depends(get_country_crud)) -> List[Country]:
    """Get a list of all countries.

    Args:
        crud (CountryCRUD, optional): The CRUD instance. Defaults to Depends(get_country_crud).

    Returns:
        List[Country]: A list of all countries.
    """
    return await crud.get_countries()

@router.get("/countries/{country_id}", response_model=Country, responses={
    404: {"description": "Country not found"}})
async def read_country(country_id: int, crud: CountryCRUD = Depends(get_country_crud)) -> Country:
    """Get a country by its ID.

    Args:
        country_id (int): The ID of the country to retrieve.
        crud (CountryCRUD, optional): The CRUD instance. Defaults to Depends(get_country_crud).

    Raises:
        HTTPException: If the country with the given ID is not found.

    Returns:
        Country: The country with the given ID.
    """
    country = await crud.get_country(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@router.delete("/countries/{country_id}", status_code=204, responses={
    204: {"description": "Country successfully deleted"},
    404: {"description": "Country not found"}})
async def delete_country(country_id: int, crud: CountryCRUD = Depends(get_country_crud)) -> None:
    """Delete a country by its ID.

    Args:
        country_id (int): The ID of the country to delete.
        crud (CountryCRUD, optional): The CRUD instance. Defaults to Depends(get_country_crud).

    Raises:
        HTTPException: If the country with the given ID is not found.

    Returns:
        None: Indicates successful deletion.
    """
    country = await crud.delete_country(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return None

@router.put("/countries/{country_id}", response_model=Country, responses={
    200: {"description": "Country successfully updated"}, 
    404: {"description": "Country not found"}})
async def update_country(country_id: int, country: CountryCreate, crud: CountryCRUD = Depends(get_country_crud)) -> Country:
    """Update a country by its ID.

    Args:
        country_id (int): The ID of the country to update.
        country (CountryCreate): The new data for the country.
        crud (CountryCRUD, optional): The CRUD instance. Defaults to Depends(get_country_crud).

    Raises:
        HTTPException: If the country with the given ID is not found.

    Returns:
        Country: The updated country.
    """
    updated_country = await crud.update_country(country_id, country)
    if not updated_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return updated_country

@router.patch("/countries/{country_id}", response_model=Country, responses={
    200: {"description": "Country successfully partially updated"}, 
    404: {"description": "Country not found"}})
async def partial_update_country(country_id: int, country: CountryUpdate, crud: CountryCRUD = Depends(get_country_crud)) -> Country:
    """Partially update a country by its ID.

    Args:
        country_id (int): The ID of the country to update.
        country (CountryUpdate): The partial data for the country.
        crud (CountryCRUD, optional): The CRUD instance. Defaults to Depends(get_country_crud).

    Raises:
        HTTPException: If the country with the given ID is not found.

    Returns:
        Country: The updated country.
    """
    updated_country = await crud.partial_update_country(country_id, country)
    if not updated_country:
        raise HTTPException(status_code=404, detail="Country not found")
    return updated_country