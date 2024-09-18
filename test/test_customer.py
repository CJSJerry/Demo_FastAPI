from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_customers():
    response = client.get("/v1/customers")
    assert response.status_code == 200

def test_get_customer():
    response = client.get("/v1/customers/1000")
    assert response.status_code == 200
    response = client.get("/v1/customers/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}
    response = client.get(f"/v1/customers/{'string'}")
    assert response.status_code == 422

def test_post_customer_success():
    response = client.post(
        "/v1/customers/",
        json={"id": 9999, "name": "Test User", "email": "testuser@test.com", "country_id": 1000, "premium_customer": "no"}
    )
    assert response.status_code == 201
    assert response.json() == {"id": 9999, "name": "Test User", "email": "testuser@test.com", "country_id": 1000, "premium_customer": "no"}

    response = client.get("/v1/customers/9999")
    assert response.status_code == 200

def test_post_customer_conflict():
    response = client.post(
        "/v1/customers/",
        json={"id": 1000, "name": "Duplicate User", "email": "duplicate@test.com", "country_id": 1001, "premium_customer": "no"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Customer with id 1000 already exists."}

def test_post_customer_invalid():
    response = client.post(
        "/v1/customers/",
        json={"id": 9998, "name": 123, "email": "invalid@test.com", "country_id": 999, "premium_customer": [1, 2, 3]}
    )
    assert response.status_code == 422

def test_put_customer_success():
    response = client.put(
        "/v1/customers/9999",
        json={"id": 9999, "name": "Updated User", "email": "updateduser@test.com", "country_id": 1000, "premium_customer": "yes"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "name": "Updated User", "email": "updateduser@test.com", "country_id": 1000, "premium_customer": "yes"}

def test_put_customer_failed():
    response = client.put(
        "/v1/customers/9998",
        json={"id": 9998, "name": "Nonexistent User", "email": "nonexistent@test.com", "country_id": 1000, "premium_customer": "no"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}

def test_put_customer_invalid():
    response = client.put(
        "/v1/customers/9999",
        json={"id": 9999, "name": 123, "email": "invalid@test.com", "country_id": 1000, "premium_customer": [1, 2, 3]}
    )
    assert response.status_code == 422

def test_patch_customer_success():
    response = client.patch(
        "/v1/customers/9999",
        json={"name": "Partially Updated User"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "name": "Partially Updated User", "email": "updateduser@test.com", "country_id": 1000, "premium_customer": "yes"}

def test_patch_customer_failed():
    response = client.patch(
        "/v1/customers/9998",
        json={"name": "Nonexistent User"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}

def test_patch_customer_invalid():
    response = client.patch(
        "/v1/customers/9999",
        json={"name": 123, "email": "invalid@test.com"}
    )
    assert response.status_code == 422

def test_delete_customer_success():
    response = client.delete("/v1/customers/9999")
    assert response.status_code == 204

    response = client.get("/v1/customers/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}

def test_delete_customer_failed():
    response = client.delete("/v1/customers/9998")
    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}

def test_delete_customer_invalid():
    response = client.delete(f"/v1/customers/{'string'}")
    assert response.status_code == 422