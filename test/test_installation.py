from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_installations():
    response = client.get("/v1/installations")
    assert response.status_code == 200

def test_get_installation():
    response = client.get("/v1/installations/1000")
    assert response.status_code == 200
    response = client.get("/v1/installations/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Installation not found"}
    response = client.get(f"/v1/installations/{'string'}")
    assert response.status_code == 422

def test_post_installation_success():
    response = client.post(
        "/v1/installations/",
        json={"id": 9999, "name": "Inst-99999", "description": "Test Installation", "product_id": 1000, "customer_id": 1000, "installation_date": "2023-01-01"}
    )
    assert response.status_code == 201
    assert response.json() == {"id": 9999, "name": "Inst-99999", "description": "Test Installation", "product_id": 1000, "customer_id": 1000, "installation_date": "2023-01-01"}

    response = client.get("/v1/installations/9999")
    assert response.status_code == 200

def test_post_installation_conflict():
    response = client.post(
        "/v1/installations/",
        json={"id": 1000, "name": "Inst-00000", "description": "Duplicate Installation", "product_id": 1000, "customer_id": 1000, "installation_date": "2023-01-01"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Installation with id 1000 already exists."}

def test_post_installation_invalid():
    response = client.post(
        "/v1/installations/",
        json={"id": 9998, "name": 123, "description": "Invalid Installation", "product_id": "invalid", "customer_id": "invalid", "installation_date": "invalid"}
    )
    assert response.status_code == 422

def test_put_installation_success():
    response = client.put(
        "/v1/installations/9999",
        json={"id": 9999, "name": "Inst-99999", "description": "Updated Installation", "product_id": 1000, "customer_id": 1000, "installation_date": "2023-01-02"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "name": "Inst-99999", "description": "Updated Installation", "product_id": 1000, "customer_id": 1000, "installation_date": "2023-01-02"}

def test_put_installation_failed():
    response = client.put(
        "/v1/installations/9998",
        json={"id": 9998, "name": "Inst-00000", "description": "Nonexistent Installation", "product_id": 1000, "customer_id": 1000, "installation_date": "2023-01-02"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Installation not found"}

def test_put_installation_invalid():
    response = client.put(
        "/v1/installations/9999",
        json={"id": 9999, "name": 123, "description": "Invalid Installation", "product_id": "invalid", "customer_id": "invalid", "installation_date": "invalid"}
    )
    assert response.status_code == 422

def test_patch_installation_success():
    response = client.patch(
        "/v1/installations/9999",
        json={"description": "Partially Updated Installation"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "name": "Inst-99999", "description": "Partially Updated Installation", "product_id": 1000, "customer_id": 1000, "installation_date": "2023-01-02"}

def test_patch_installation_failed():
    response = client.patch(
        "/v1/installations/9998",
        json={"description": "Nonexistent Installation"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Installation not found"}

def test_patch_installation_invalid():
    response = client.patch(
        "/v1/installations/9999",
        json={"description": 123}
    )
    assert response.status_code == 422

def test_delete_installation_success():
    response = client.delete("/v1/installations/9999")
    assert response.status_code == 204

    response = client.get("/v1/installations/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Installation not found"}

def test_delete_installation_failed():
    response = client.delete("/v1/installations/9998")
    assert response.status_code == 404
    assert response.json() == {"detail": "Installation not found"}

def test_delete_installation_invalid():
    response = client.delete(f"/v1/installations/{'string'}")
    assert response.status_code == 422