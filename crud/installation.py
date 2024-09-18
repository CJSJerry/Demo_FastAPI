from asyncpg.exceptions import UniqueViolationError
from models.installation import Installation, InstallationCreate, InstallationUpdate
from asyncpg import Connection
from typing import List, Optional

class InstallationCRUD:
    """CRUD operations for Installation.

    Attributes:
        db (Connection): The database connection.
    """
    def __init__(self, db: Connection) -> None:
        """Initialize the CRUD instance.

        Args:
            db (Connection): The database connection.
        """
        self.db = db

    async def create_installation(self, installation: InstallationCreate) -> Optional[Installation]:
        """Create a new installation.

        Args:
            installation (InstallationCreate): The installation data to create.

        Returns:
            Optional[Installation]: The created installation or None if a UniqueViolationError occurs.
        """
        query = """
        INSERT INTO installation (id, name, description, product_id, customer_id, installation_date)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, name, description, product_id, customer_id, installation_date
        """
        try:
            row = await self.db.fetchrow(query, installation.id, installation.name, installation.description, installation.product_id, installation.customer_id, installation.installation_date)
            return Installation(**row)
        except UniqueViolationError:
            return None

    async def get_installations(self) -> List[Installation]:
        """Get all installations.

        Returns:
            List[Installation]: A list of all installations.
        """
        query = "SELECT id, name, description, product_id, customer_id, installation_date FROM installation"
        rows = await self.db.fetch(query)
        return [Installation(**row) for row in rows]

    async def get_installation(self, installation_id: int) -> Optional[Installation]:
        """Get an installation by its ID.

        Args:
            installation_id (int): The ID of the installation to retrieve.

        Returns:
            Optional[Installation]: The installation with the given ID or None if not found.
        """
        query = "SELECT id, name, description, product_id, customer_id, installation_date FROM installation WHERE id = $1"
        row = await self.db.fetchrow(query, installation_id)
        if not row:
            return None
        return Installation(**row)

    async def delete_installation(self, installation_id: int) -> Optional[Installation]:
        """Delete an installation by its ID.

        Args:
            installation_id (int): The ID of the installation to delete.

        Returns:
            Optional[Installation]: The deleted installation or None if not found.
        """
        query = "DELETE FROM installation WHERE id = $1 RETURNING id, name, description, product_id, customer_id, installation_date"
        row = await self.db.fetchrow(query, installation_id)
        if not row:
            return None
        return Installation(**row)

    async def update_installation(self, installation_id: int, installation: InstallationCreate) -> Optional[Installation]:
        """Update an installation by its ID.

        Args:
            installation_id (int): The ID of the installation to update.
            installation (InstallationCreate): The new data for the installation.

        Returns:
            Optional[Installation]: The updated installation or None if not found.
        """
        query = """
        UPDATE installation
        SET name = $2, description = $3, product_id = $4, customer_id = $5, installation_date = $6
        WHERE id = $1
        RETURNING id, name, description, product_id, customer_id, installation_date
        """
        row = await self.db.fetchrow(query, installation_id, installation.name, installation.description, installation.product_id, installation.customer_id, installation.installation_date)
        if not row:
            return None
        return Installation(**row)

    async def partial_update_installation(self, installation_id: int, installation: InstallationUpdate) -> Optional[Installation]:
        """Partially update an installation by its ID.

        Args:
            installation_id (int): The ID of the installation to update.
            installation (InstallationUpdate): The partial data for the installation.

        Returns:
            Optional[Installation]: The updated installation or None if not found.
        """
        query = """
        UPDATE installation
        SET name = COALESCE($2, name), description = COALESCE($3, description), product_id = COALESCE($4, product_id), customer_id = COALESCE($5, customer_id), installation_date = COALESCE($6, installation_date)
        WHERE id = $1
        RETURNING id, name, description, product_id, customer_id, installation_date
        """
        row = await self.db.fetchrow(query, installation_id, installation.name, installation.description, installation.product_id, installation.customer_id, installation.installation_date)
        if not row:
            return None
        return Installation(**row)