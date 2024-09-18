from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_products():
    response = client.get("/v1/products")
    assert response.status_code == 200

def test_get_product():
    response = client.get("/v1/products/1000")
    assert response.status_code == 200
    response = client.get("/v1/products/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
    response = client.get(f"/v1/products/{'string'}")
    assert response.status_code == 422

def test_post_product_success():
    response = client.post(
        "/v1/products/",
        json={"id": 9999, "reference": "Prd-99999", "name": "Test Product", "category_id": 1000, "price": "100"}
    )
    assert response.status_code == 201
    assert response.json() == {"id": 9999, "reference": "Prd-99999", "name": "Test Product", "category_id": 1000, "price": "100"}

    response = client.get("/v1/products/9999")
    assert response.status_code == 200

def test_post_product_conflict():
    response = client.post(
        "/v1/products/",
        json={"id": 1000, "reference": "Prd-00000", "name": "Duplicate Product", "category_id": 1000, "price": "200"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Product with id 1000 already exists."}

def test_post_product_invalid():
    response = client.post(
        "/v1/products/",
        json={"id": 9998, "reference": 123, "name": "Invalid Product", "category_id": 1000, "price": "invalid"}
    )
    assert response.status_code == 422

def test_put_product_success():
    response = client.put(
        "/v1/products/9999",
        json={"id": 9999, "reference": "Prd-99999", "name": "Updated Product", "category_id": 1000, "price": "150"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "reference": "Prd-99999", "name": "Updated Product", "category_id": 1000, "price": "150"}

def test_put_product_failed():
    response = client.put(
        "/v1/products/9998",
        json={"id": 9998, "reference": "Prd-00000", "name": "Nonexistent Product", "category_id": 1000, "price": "200"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_put_product_invalid():
    response = client.put(
        "/v1/products/9999",
        json={"id": 9999, "reference": 123, "name": "Invalid Product", "category_id": 1000, "price": "invalid"}
    )
    assert response.status_code == 422

def test_patch_product_success():
    response = client.patch(
        "/v1/products/9999",
        json={"name": "Partially Updated Product"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "reference": "Prd-99999", "name": "Partially Updated Product", "category_id": 1000, "price": "150"}

def test_patch_product_failed():
    response = client.patch(
        "/v1/products/9998",
        json={"name": "Nonexistent Product"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_patch_product_invalid():
    response = client.patch(
        "/v1/products/9999",
        json={"name": 123}
    )
    assert response.status_code == 422

def test_delete_product_success():
    response = client.delete("/v1/products/9999")
    assert response.status_code == 204

    response = client.get("/v1/products/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_delete_product_failed():
    response = client.delete("/v1/products/9998")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_delete_product_invalid():
    response = client.delete(f"/v1/products/{'string'}")
    assert response.status_code == 422