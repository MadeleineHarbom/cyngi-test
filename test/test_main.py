from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)  # Create a test client

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}

def test_get_root_fail_on_wrong_message():
    response = client.get("/")
    assert response.json() != {"message": "Hello, wørld!"}
