from asyncpg.exceptions import UniqueViolationError
from models.product_category import ProductCategory, ProductCategoryCreate, ProductCategoryUpdate
from asyncpg import Connection
from typing import List, Optional

class ProductCategoryCRUD:
    """CRUD operations for ProductCategory.

    Attributes:
        db (Connection): The database connection.
    """
    def __init__(self, db: Connection) -> None:
        """Initialize the CRUD instance.

        Args:
            db (Connection): The database connection.
        """
        self.db = db

    async def create_product_category(self, category: ProductCategoryCreate) -> Optional[ProductCategory]:
        """Create a new product category.

        Args:
            category (ProductCategoryCreate): The product category data to create.

        Returns:
            Optional[ProductCategory]: The created product category or None if a UniqueViolationError occurs.
        """
        query = """
        INSERT INTO product_category (id, name)
        VALUES ($1, $2)
        RETURNING id, name
        """
        try:
            row = await self.db.fetchrow(query, category.id, category.name)
            return ProductCategory(**row)
        except UniqueViolationError:
            return None

    async def get_product_categories(self) -> List[ProductCategory]:
        """Get all product categories.

        Returns:
            List[ProductCategory]: A list of all product categories.
        """
        query = "SELECT id, name FROM product_category"
        rows = await self.db.fetch(query)
        return [ProductCategory(**row) for row in rows]

    async def get_product_category(self, category_id: int) -> Optional[ProductCategory]:
        """Get a product category by its ID.

        Args:
            category_id (int): The ID of the product category to retrieve.

        Returns:
            Optional[ProductCategory]: The product category with the given ID or None if not found.
        """
        query = "SELECT id, name FROM product_category WHERE id = $1"
        row = await self.db.fetchrow(query, category_id)
        if not row:
            return None
        return ProductCategory(**row)

    async def delete_product_category(self, category_id: int) -> Optional[ProductCategory]:
        """Delete a product category by its ID.

        Args:
            category_id (int): The ID of the product category to delete.

        Returns:
            Optional[ProductCategory]: The deleted product category or None if not found.
        """
        query = "DELETE FROM product_category WHERE id = $1 RETURNING id, name"
        row = await self.db.fetchrow(query, category_id)
        if not row:
            return None
        return ProductCategory(**row)

    async def update_product_category(self, category_id: int, category: ProductCategoryCreate) -> Optional[ProductCategory]:
        """Update a product category by its ID.

        Args:
            category_id (int): The ID of the product category to update.
            category (ProductCategoryCreate): The new data for the product category.

        Returns:
            Optional[ProductCategory]: The updated product category or None if not found.
        """
        query = """
        UPDATE product_category
        SET name = $2
        WHERE id = $1
        RETURNING id, name
        """
        row = await self.db.fetchrow(query, category_id, category.name)
        if not row:
            return None
        return ProductCategory(**row)

    async def partial_update_product_category(self, category_id: int, category: ProductCategoryUpdate) -> Optional[ProductCategory]:
        """Partially update a product category by its ID.

        Args:
            category_id (int): The ID of the product category to update.
            category (ProductCategoryUpdate): The partial data for the product category.

        Returns:
            Optional[ProductCategory]: The updated product category or None if not found.
        """
        query = """
        UPDATE product_category
        SET name = COALESCE($2, name)
        WHERE id = $1
        RETURNING id, name
        """
        row = await self.db.fetchrow(query, category_id, category.name)
        if not row:
            return None
        return ProductCategory(**row)