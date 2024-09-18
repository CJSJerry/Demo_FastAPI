from asyncpg.exceptions import UniqueViolationError
from models.country import Country, CountryCreate, CountryUpdate
from asyncpg import Connection
from typing import List, Optional

class CountryCRUD:
    """CRUD operations for Country.

    Attributes:
        db (Connection): The database connection.
    """
    def __init__(self, db: Connection) -> None:
        """Initialize the CRUD instance.

        Args:
            db (Connection): The database connection.
        """
        self.db = db

    async def create_country(self, country: CountryCreate) -> Optional[Country]:
        """Create a new country.

        Args:
            country (CountryCreate): The country data to create.

        Returns:
            Optional[Country]: The created country or None if a UniqueViolationError occurs.
        """
        query = """
        INSERT INTO country (id, name, region)
        VALUES ($1, $2, $3)
        RETURNING id, name, region
        """
        try:
            row = await self.db.fetchrow(query, country.id, country.name, country.region)
            return Country(**row)
        except UniqueViolationError:
            return None

    async def get_countries(self) -> List[Country]:
        """Get all countries.

        Returns:
            List[Country]: A list of all countries.
        """
        query = "SELECT id, name, region FROM country"
        rows = await self.db.fetch(query)
        return [Country(**row) for row in rows]

    async def get_country(self, country_id: int) -> Optional[Country]:
        """Get a country by its ID.

        Args:
            country_id (int): The ID of the country to retrieve.

        Returns:
            Optional[Country]: The country with the given ID or None if not found.
        """
        query = "SELECT id, name, region FROM country WHERE id = $1"
        row = await self.db.fetchrow(query, country_id)
        if not row:
            return None
        return Country(**row)

    async def delete_country(self, country_id: int) -> Optional[Country]:
        """Delete a country by its ID.

        Args:
            country_id (int): The ID of the country to delete.

        Returns:
            Optional[Country]: The deleted country or None if not found.
        """
        query = "DELETE FROM country WHERE id = $1 RETURNING id, name, region"
        row = await self.db.fetchrow(query, country_id)
        if not row:
            return None
        return Country(**row)

    async def update_country(self, country_id: int, country: CountryCreate) -> Optional[Country]:
        """Update a country by its ID.

        Args:
            country_id (int): The ID of the country to update.
            country (CountryCreate): The new data for the country.

        Returns:
            Optional[Country]: The updated country or None if not found.
        """
        query = """
        UPDATE country
        SET name = $2, region = $3
        WHERE id = $1
        RETURNING id, name, region
        """
        row = await self.db.fetchrow(query, country_id, country.name, country.region)
        if not row:
            return None
        return Country(**row)

    async def partial_update_country(self, country_id: int, country: CountryUpdate) -> Optional[Country]:
        """Partially update a country by its ID.

        Args:
            country_id (int): The ID of the country to update.
            country (CountryUpdate): The partial data for the country.

        Returns:
            Optional[Country]: The updated country or None if not found.
        """
        query = """
        UPDATE country
        SET name = COALESCE($2, name), region = COALESCE($3, region)
        WHERE id = $1
        RETURNING id, name, region
        """
        row = await self.db.fetchrow(query, country_id, country.name, country.region)
        if not row:
            return None
        return Country(**row)