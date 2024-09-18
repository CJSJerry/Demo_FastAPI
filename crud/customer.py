from asyncpg.exceptions import UniqueViolationError
from models.customer import Customer, CustomerCreate, CustomerUpdate
from asyncpg import Connection
from typing import List, Optional

class CustomerCRUD:
    """CRUD operations for Customer.

    Attributes:
        db (Connection): The database connection.
    """
    def __init__(self, db: Connection) -> None:
        """Initialize the CRUD instance.

        Args:
            db (Connection): The database connection.
        """
        self.db = db

    async def create_customer(self, customer: CustomerCreate) -> Optional[Customer]:
        """Create a new customer.

        Args:
            customer (CustomerCreate): The customer data to create.

        Returns:
            Optional[Customer]: The created customer or None if a UniqueViolationError occurs.
        """
        query = """
        INSERT INTO customer (id, name, email, country_id, premium_customer)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, name, email, country_id, premium_customer
        """
        try:
            row = await self.db.fetchrow(query, customer.id, customer.name, customer.email, customer.country_id, customer.premium_customer)
            return Customer(**row)
        except UniqueViolationError:
            return None

    async def get_customers(self) -> List[Customer]:
        """Get all customers.

        Returns:
            List[Customer]: A list of all customers.
        """
        query = "SELECT id, name, email, country_id, premium_customer FROM customer"
        rows = await self.db.fetch(query)
        return [Customer(**row) for row in rows]

    async def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get a customer by its ID.

        Args:
            customer_id (int): The ID of the customer to retrieve.

        Returns:
            Optional[Customer]: The customer with the given ID or None if not found.
        """
        query = "SELECT id, name, email, country_id, premium_customer FROM customer WHERE id = $1"
        row = await self.db.fetchrow(query, customer_id)
        if not row:
            return None
        return Customer(**row)

    async def delete_customer(self, customer_id: int) -> Optional[Customer]:
        """Delete a customer by its ID.

        Args:
            customer_id (int): The ID of the customer to delete.

        Returns:
            Optional[Customer]: The deleted customer or None if not found.
        """
        query = "DELETE FROM customer WHERE id = $1 RETURNING id, name, email, country_id, premium_customer"
        row = await self.db.fetchrow(query, customer_id)
        if not row:
            return None
        return Customer(**row)

    async def update_customer(self, customer_id: int, customer: CustomerCreate) -> Optional[Customer]:
        """Update a customer by its ID.

        Args:
            customer_id (int): The ID of the customer to update.
            customer (CustomerCreate): The new data for the customer.

        Returns:
            Optional[Customer]: The updated customer or None if not found.
        """
        query = """
        UPDATE customer
        SET name = $2, email = $3, country_id = $4, premium_customer = $5
        WHERE id = $1
        RETURNING id, name, email, country_id, premium_customer
        """
        row = await self.db.fetchrow(query, customer_id, customer.name, customer.email, customer.country_id, customer.premium_customer)
        if not row:
            return None
        return Customer(**row)

    async def partial_update_customer(self, customer_id: int, customer: CustomerUpdate) -> Optional[Customer]:
        """Partially update a customer by its ID.

        Args:
            customer_id (int): The ID of the customer to update.
            customer (CustomerUpdate): The partial data for the customer.

        Returns:
            Optional[Customer]: The updated customer or None if not found.
        """
        query = """
        UPDATE customer
        SET name = COALESCE($2, name), email = COALESCE($3, email), country_id = COALESCE($4, country_id), premium_customer = COALESCE($5, premium_customer)
        WHERE id = $1
        RETURNING id, name, email, country_id, premium_customer
        """
        row = await self.db.fetchrow(query, customer_id, customer.name, customer.email, customer.country_id, customer.premium_customer)
        if not row:
            return None
        return Customer(**row)