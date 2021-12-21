import pytest
from app.database import  Base
from app.main import app
from app import schemas
from app.config import settings

from jose import  jwt




def test_root(client):
    res = client.get("/")
    print(res.json())
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to api'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/api/v1/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    print(res)
    print(res.status_code)
    print(res.json())
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

# here the login test is dependednt on the above test case 
# Each and every test should be independent 

def test_user_login(client, create_test_user):
    res = client.post(
        "/api/v1/auth/login", data={"username": create_test_user['email'], "password": create_test_user['password']})
    print(res)
    print(res.status_code)
    print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.Token , settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert id == create_test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('hello456@gmail1.com', 'password1123',403),
    ('hello456@gmail1.com', 'password1123',403),
    ('wrong@gmail1.com', 'password1123',403),
    (None, 'password1123',422)
])
def test_incorrect_login(create_test_user, client, email, password, status_code):
    res = client.post("/api/v1/auth/login", data={"username": email, "password": password})
    assert res.status_code == status_code 
    #assert res.json().get('detail') == 'Invalid Credentials' 


