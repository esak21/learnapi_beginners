from fastapi.testclient import TestClient

from app.database import get_db, Base
from app.oauth2 import create_access_token
from app.main import app
from app import models
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from jose import JWTError, jwt
import  pytest

TEST_HOST_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/${settings.database_name}'
# create Engine 
engine = create_engine(TEST_HOST_URL)

print(f"INFO:: USERNAME ::{settings.database_username}")
print(f"INFO:: PASSWORD ::{settings.database_password}")
print(f"INFO:: HOSTNAME ::{settings.database_hostname}")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# Creating a Fixture 
# this will create a user in the database 
@pytest.fixture()
def create_test_user(client):

    user_data = {
        "email": "hello456@gmail.com",
        "password": "password123"
    }
    res = client.post("/api/v1/users/", json=user_data)
    assert res.status_code == 201 
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture()
def token(create_test_user):
    return create_access_token({"user_id": create_test_user['id']})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client 


@pytest.fixture
def create_posts(create_test_user, session):
    posts_data = [
        {
            "title": "First Title",
            "content":" My First Ever Blog",
            "user_id": create_test_user['id']
        },{
            "title": "Second Title",
            "content":" My Second Ever Blog",
            "user_id": create_test_user['id']
        },{
            "title": "Third Title",
            "content":" My Third Ever Blog",
            "user_id": create_test_user['id']
        }
    ]

    def create_post_model(postdata):
        return models.Post(**postdata)

    postmap = map(create_post_model, posts_data)
    posts = list(postmap)
    session.add_all(posts)

    session.commit()

    return session.query(models.Post).all()