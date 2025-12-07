import pytest
import allure
import json
import requests
from endpoints.authorization import Authorization
from endpoints.baseapi import BaseAPI
from endpoints.create_meme import CreateMeme
from endpoints.delete_meme import DeleteMeme
from endpoints.get_meme import GetMeme
from endpoints.update_meme import UpdateMeme


@pytest.fixture(scope="session")
def sample_user_name():
    user_name = "test_user"
    return user_name


@pytest.fixture(scope="session", autouse=True)
def auth_token(sample_user_name):
    auth = Authorization()

    if BaseAPI.token:
        resp = auth.is_alive(BaseAPI.token)
        if resp.status_code == 200:
            print("Используется существующий валидный токен")
            return BaseAPI.token
    print("Получение нового токена...")
    response = auth.authorization({"name": {sample_user_name}})
    assert response.status_code == 200, "Не удалось получить токен авторизации"
    return BaseAPI.token


@pytest.fixture(scope="session")
def create_meme():
    return CreateMeme()


@pytest.fixture()
def sample_meme_payload():
    return {
        "text": "Test meme text",
        "url": "https://example.com/meme.jpg",
        "tags": ["funny", "test"],
        "info": {
            "colors": ["red", "blue"],
            "objects": ["text", "image"]
        }
    }


@pytest.fixture()
def created_meme_id(create_meme, sample_meme_payload, delete_meme):
    response = create_meme.create_new_meme(sample_meme_payload)
    meme_id = response.json()['id']
    yield meme_id
    delete_meme.delete_meme_by_id(meme_id)


@pytest.fixture(scope="session", autouse=True)
def update_meme():
    return UpdateMeme()


@pytest.fixture(scope="session", autouse=True)
def get_meme():
    return GetMeme()


@pytest.fixture(scope="session", autouse=True)
def delete_meme():
    return DeleteMeme()


@pytest.fixture()
def attach_response():
    def attach(response, name="Request/Response"):
        allure.attach(
            f"{response.request.method} {response.request.url}\n\n"
            f"Request body:\n{response.request.body}",
            name=f"{name} - Request",
            attachment_type=allure.attachment_type.JSON
        )

        allure.attach(
            f"Status code: {response.status_code}\n\nResponse body:\n{response.text}",
            name=f"{name} - Response",
            attachment_type=allure.attachment_type.JSON
        )

        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            return response.text
    return attach


@pytest.fixture
def check_status_code():
    def check(response, expected_status=200):
        assert response.status_code == expected_status, (
            f"Ожидался статус {expected_status}, получен {response.status_code}"
        )

        if response.text:
            allure.attach(
                f"Status code: {response.status_code}\n\nResponse body:\n{response.text}",
                name="Response",
                attachment_type=allure.attachment_type.TEXT
            )

    return check