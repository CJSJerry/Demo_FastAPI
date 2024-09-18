from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get():
    response = client.get("/v1/countries")
    assert response.status_code == 200

def test_get_all():
    # Assuming the country with id 1000 already exists in the initial data
    response = client.get("/v1/countries/1000")
    assert response.status_code == 200
    response = client.get("/v1/countries/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}
    response = client.get(f"/v1/countries/{'string'}")
    assert response.status_code == 422

def test_post_success():
    response = client.post(
        "/v1/countries/",
        json={"id": 9999, "name": "Testland", "region": "TestRegion"}
    )
    assert response.status_code == 201
    assert response.json() == {"id": 9999, "name": "Testland", "region": "TestRegion"}

    # Verify it was created
    response = client.get("/v1/countries/9999")
    assert response.status_code == 200

def test_post_conflict():
    # Assuming the country with id 1000 already exists in the initial data
    response = client.post(
        "/v1/countries/",
        json={"id": 1000, "name": "DuplicateCountry", "region": "DuplicateRegion"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Country with id 1000 already exists."}

def test_post_invalid():
    response = client.post(
        "/v1/countries/",
        json={"id": 9998, "name": 123, "region": [1, 2, 3]}
    )
    assert response.status_code == 422

def test_put_success():
    response = client.put(
        "/v1/countries/9999",
        json={"id": 9999, "name": "TestCountry", "region": "TestRegion"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "name": "TestCountry", "region": "TestRegion"}

def test_put_failed():
    response = client.put(
        "/v1/countries/9998",
        json={"id": 9998, "name": "TestCountry", "region": "TestRegion"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}

def test_put_invalid():
    response = client.put(
        "/v1/countries/9999",
        json={"id": 9999, "name": 123, "region": [1, 2, 3]}
    )
    assert response.status_code == 422

def test_patch_success():
    response = client.patch(
        "/v1/countries/9999",
        json={"name": "Testland"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 9999, "name": "Testland", "region": "TestRegion"}

def test_patch_failed():
    response = client.patch(
        "/v1/countries/9998",
        json={"name": "Testland"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}

def test_patch_invalid():
    response = client.patch(
        "/v1/countries/9999",
        json={"name": 123, "region": [1, 2, 3]}
    )
    assert response.status_code == 422

def test_delete_success():
    # Delete the country with id 9999 created earlier
    response = client.delete("/v1/countries/9999")
    assert response.status_code == 204

    # Verify it was deleted
    response = client.get("/v1/countries/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}

def test_delete_failed():
    response = client.delete("/v1/countries/9998")
    assert response.status_code == 404
    assert response.json() == {"detail": "Country not found"}

def test_delete_invalid():
    response = client.delete(f"/v1/countries/{'string'}")
    assert response.status_code == 422

# pytest test/test_country.py -v