from asyncpg.exceptions import UniqueViolationError
from models.product import Product, ProductCreate, ProductUpdate
from asyncpg import Connection
from typing import List, Optional

class ProductCRUD:
    """CRUD operations for Product.

    Attributes:
        db (Connection): The database connection.
    """
    def __init__(self, db: Connection) -> None:
        """Initialize the CRUD instance.

        Args:
            db (Connection): The database connection.
        """
        self.db = db

    async def create_product(self, product: ProductCreate) -> Optional[Product]:
        """Create a new product.

        Args:
            product (ProductCreate): The product data to create.

        Returns:
            Optional[Product]: The created product or None if a UniqueViolationError occurs.
        """
        query = """
        INSERT INTO product (id, reference, name, category_id, price)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, reference, name, category_id, price
        """
        try:
            row = await self.db.fetchrow(query, product.id, product.reference, product.name, product.category_id, product.price)
            return Product(**row)
        except UniqueViolationError:
            return None

    async def get_products(self) -> List[Product]:
        """Get all products.

        Returns:
            List[Product]: A list of all products.
        """
        query = "SELECT id, reference, name, category_id, price FROM product"
        rows = await self.db.fetch(query)
        return [Product(**row) for row in rows]

    async def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by its ID.

        Args:
            product_id (int): The ID of the product to retrieve.

        Returns:
            Optional[Product]: The product with the given ID or None if not found.
        """
        query = "SELECT id, reference, name, category_id, price FROM product WHERE id = $1"
        row = await self.db.fetchrow(query, product_id)
        if not row:
            return None
        return Product(**row)

    async def delete_product(self, product_id: int) -> Optional[Product]:
        """Delete a product by its ID.

        Args:
            product_id (int): The ID of the product to delete.

        Returns:
            Optional[Product]: The deleted product or None if not found.
        """
        query = "DELETE FROM product WHERE id = $1 RETURNING id, reference, name, category_id, price"
        row = await self.db.fetchrow(query, product_id)
        if not row:
            return None
        return Product(**row)

    async def update_product(self, product_id: int, product: ProductCreate) -> Optional[Product]:
        """Update a product by its ID.

        Args:
            product_id (int): The ID of the product to update.
            product (ProductCreate): The new data for the product.

        Returns:
            Optional[Product]: The updated product or None if not found.
        """
        query = """
        UPDATE product
        SET reference = $2, name = $3, category_id = $4, price = $5
        WHERE id = $1
        RETURNING id, reference, name, category_id, price
        """
        row = await self.db.fetchrow(query, product_id, product.reference, product.name, product.category_id, product.price)
        if not row:
            return None
        return Product(**row)

    async def partial_update_product(self, product_id: int, product: ProductUpdate) -> Optional[Product]:
        """Partially update a product by its ID.

        Args:
            product_id (int): The ID of the product to update.
            product (ProductUpdate): The partial data for the product.

        Returns:
            Optional[Product]: The updated product or None if not found.
        """
        query = """
        UPDATE product
        SET reference = COALESCE($2, reference), name = COALESCE($3, name), category_id = COALESCE($4, category_id), price = COALESCE($5, price)
        WHERE id = $1
        RETURNING id, reference, name, category_id, price
        """
        row = await self.db.fetchrow(query, product_id, product.reference, product.name, product.category_id, product.price)
        if not row:
            return None
        return Product(**row)