from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_product_categories():
    response = client.get("/v1/product_categories")
    assert response.status_code == 200

def test_get_product_category():
    response = client.get("/v1/product_categories/1000")
    assert response.status_code == 200
    response = client.get("/v1/product_categories/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product category not found"}
    response = client.get(f"/v1/product_categories/{'string'}")
    assert response.status_code == 422

def test_post_product_category_success():
    response = client.post(
        "/v1/product_categories/",
        json={"id": 9999, "name": "Test Category"}
    )
    assert response.status_code == 201
    assert response.json() == {"id": 9999, "name": "Test Category"}

    response = client.get("/v1/product_categories/9999")
    assert response.status_code == 200

def test_post_product_category_conflict():
    response = client.post(
        "/v1/product_categories/",
        json={"id": 1000, "name": "Duplicate Category"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Product category with id 1000 already exists."}

def test_post_product_category_invalid():
    response = client.post(
        "/v1/product_categories/",
        json={"id": 9998, "name": 123}
    )
    assert response.status_code == 422

def test_put_product_category_success():
    response = client.put(
        "/v1/product_categories/9999",
        json={"id": 9999, "name": "Updated Category"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "name": "Updated Category"}

def test_put_product_category_failed():
    response = client.put(
        "/v1/product_categories/9998",
        json={"id": 9998, "name": "Nonexistent Category"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Product category not found"}

def test_put_product_category_invalid():
    response = client.put(
        "/v1/product_categories/9999",
        json={"id": 9999, "name": 123}
    )
    assert response.status_code == 422

def test_patch_product_category_success():
    response = client.patch(
        "/v1/product_categories/9999",
        json={"name": "Partially Updated Category"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "name": "Partially Updated Category"}

def test_patch_product_category_failed():
    response = client.patch(
        "/v1/product_categories/9998",
        json={"name": "Nonexistent Category"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Product category not found"}

def test_patch_product_category_invalid():
    response = client.patch(
        "/v1/product_categories/9999",
        json={"name": 123}
    )
    assert response.status_code == 422

def test_delete_product_category_success():
    response = client.delete("/v1/product_categories/9999")
    assert response.status_code == 204

    response = client.get("/v1/product_categories/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product category not found"}

def test_delete_product_category_failed():
    response = client.delete("/v1/product_categories/9998")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product category not found"}

def test_delete_product_category_invalid():
    response = client.delete(f"/v1/product_categories/{'string'}")
    assert response.status_code == 422