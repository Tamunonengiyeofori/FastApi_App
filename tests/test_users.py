# from .db import session, client
from app import schemas
import pytest
from app.config import settings
from app.Oauth2 import SECRET_KEY
from jose import jwt


# # Testing the root path operation
# def test_root(client):
#     response = client.get("/")
#     print(response.json().get("message"))
#     assert response.json().get("message") == "BIND MOUNT WORKS"
#     assert response.status_code == 200


# Resting user creation function
def test_create_user(client):
    res = client.post("/users/", 
                      json={
                          "email":"kenn@kenn.com",
                          "password":"qwerty1234"
                      }
                      )
    new_user = schemas.UserOut(**res.json())
    # print(res.json())
    assert new_user.email == "kenn@kenn.com"
    assert res.status_code == 201
    
def test_login_user(client, test_user):
    res = client.post("/login", 
                       data={
                           "username": test_user["email"],
                           "password":test_user["password"]
                       })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200 
    
@pytest.mark.parametrize("email, password, status_code", [
                         ("kenn@tammy.com", "qwertydad", 403),
                         ("sanajay@gmail.com", "qwertydad", 403),
                         ("tond@gmail.com", "qwertydad", 403),
                         (None, "sanjeev1234", 422),
                         ("sanjeev1234@gmail.com", None, 422)
                         ]
                        )
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login",
                 data={
                     "username": email,
                     "password":password}
                )
    print(res.json())
    assert res.status_code == status_code 
    # assert res.json().get("detail") == "Invalid Credentials"