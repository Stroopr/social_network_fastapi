from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users/", json={"email":"test_user_tested2@gmail.com","username":"test_user_tested2" ,"password":"password123"})
    print(res.json)
    assert res.status_code == 201