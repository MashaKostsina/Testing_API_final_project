import pytest
from authorization import Authorization
from endpoints.baseapi import BaseAPI


@pytest.fixture(scope="session", autouse=True)
def auth_token():
    auth = Authorization()

    if BaseAPI.token:
        resp = auth.is_alive(BaseAPI.token)
        if resp.status_code == 200:
            print("Старый токен всё ещё валиден")
            return BaseAPI.token

    print("Получение нового токена...")
    response = auth.authorization({"name": "test"})
    return BaseAPI.token
