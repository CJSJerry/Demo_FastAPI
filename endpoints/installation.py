from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.installation import Installation, InstallationCreate, InstallationUpdate
from dependencies import get_db
from crud.installation import InstallationCRUD

router = APIRouter()

def get_installation_crud(db=Depends(get_db)) -> InstallationCRUD:
    """Get an InstallationCRUD instance.

    Args:
        db (Optional[Depends]): Optional database dependency.

    Returns:
        InstallationCRUD: An instance of InstallationCRUD.
    """
    return InstallationCRUD(db)

@router.post("/installations/", response_model=Installation, status_code=201, responses={
    201: {"description": "Installation successfully created"},
    409: {"description": "Installation with this ID already exists"}})
async def create_installation(installation: InstallationCreate, crud: InstallationCRUD = Depends(get_installation_crud)) -> Installation:
    """Create a new installation.

    Args:
        installation (InstallationCreate): The installation data to create.
        crud (InstallationCRUD, optional): The CRUD instance. Defaults to Depends(get_installation_crud).

    Raises:
        HTTPException: If an installation with the given ID already exists.

    Returns:
        Installation: The created installation.
    """
    new_installation = await crud.create_installation(installation)
    if new_installation is None:
        raise HTTPException(status_code=409, detail=f"Installation with id {installation.id} already exists.")
    return new_installation

@router.get("/installations/", response_model=List[Installation])
async def read_installations(crud: InstallationCRUD = Depends(get_installation_crud)) -> List[Installation]:
    """Get a list of all installations.

    Args:
        crud (InstallationCRUD, optional): The CRUD instance. Defaults to Depends(get_installation_crud).

    Returns:
        List[Installation]: A list of all installations.
    """
    return await crud.get_installations()

@router.get("/installations/{installation_id}", response_model=Installation, responses={
    404: {"description": "Installation not found"}})
async def read_installation(installation_id: int, crud: InstallationCRUD = Depends(get_installation_crud)) -> Installation:
    """Get an installation by its ID.

    Args:
        installation_id (int): The ID of the installation to retrieve.
        crud (InstallationCRUD, optional): The CRUD instance. Defaults to Depends(get_installation_crud).

    Raises:
        HTTPException: If the installation with the given ID is not found.

    Returns:
        Installation: The installation with the given ID.
    """
    installation = await crud.get_installation(installation_id)
    if not installation:
        raise HTTPException(status_code=404, detail="Installation not found")
    return installation

@router.delete("/installations/{installation_id}", status_code=204, responses={
    204: {"description": "Installation successfully deleted"},
    404: {"description": "Installation not found"}})
async def delete_installation(installation_id: int, crud: InstallationCRUD = Depends(get_installation_crud)) -> None:
    """Delete an installation by its ID.

    Args:
        installation_id (int): The ID of the installation to delete.
        crud (InstallationCRUD, optional): The CRUD instance. Defaults to Depends(get_installation_crud).

    Raises:
        HTTPException: If the installation with the given ID is not found.
    """
    installation = await crud.delete_installation(installation_id)
    if not installation:
        raise HTTPException(status_code=404, detail="Installation not found")
    return None

@router.put("/installations/{installation_id}", response_model=Installation, responses={
    200: {"description": "Installation successfully updated"}, 
    404: {"description": "Installation not found"}})
async def update_installation(installation_id: int, installation: InstallationCreate, crud: InstallationCRUD = Depends(get_installation_crud)) -> Installation:
    """Update an installation by its ID.

    Args:
        installation_id (int): The ID of the installation to update.
        installation (InstallationCreate): The new data for the installation.
        crud (InstallationCRUD, optional): The CRUD instance. Defaults to Depends(get_installation_crud).

    Raises:
        HTTPException: If the installation with the given ID is not found.

    Returns:
        Installation: The updated installation.
    """
    updated_installation = await crud.update_installation(installation_id, installation)
    if not updated_installation:
        raise HTTPException(status_code=404, detail="Installation not found")
    return updated_installation

@router.patch("/installations/{installation_id}", response_model=Installation, responses={
    200: {"description": "Installation successfully partially updated"}, 
    404: {"description": "Installation not found"}})
async def partial_update_installation(installation_id: int, installation: InstallationUpdate, crud: InstallationCRUD = Depends(get_installation_crud)) -> Installation:
    """Partially update an installation by its ID.

    Args:
        installation_id (int): The ID of the installation to update.
        installation (InstallationUpdate): The partial data for the installation.
        crud (InstallationCRUD, optional): The CRUD instance. Defaults to Depends(get_installation_crud).

    Raises:
        HTTPException: If the installation with the given ID is not found.

    Returns:
        Installation: The updated installation.
    """
    updated_installation = await crud.partial_update_installation(installation_id, installation)
    if not updated_installation:
        raise HTTPException(status_code=404, detail="Installation not found")
    return updated_installation