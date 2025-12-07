import allure
from endpoints.baseapi import BaseAPI


class Authorization(BaseAPI):
    token = None

    @allure.step("Получение токена авторизации")
    def authorization(self, payload):
        response = self.send_request(method="POST", endpoint="/authorize", json=payload)
        data = response.json()
        token = data.get("token")
        if not token:
            raise Exception("Токен не найден в ответе!")
        BaseAPI.token = token
        return response

    @allure.step("Проверка жизни токена")
    def is_alive(self, token):
        return self.send_request(method="GET", endpoint=f"/authorize/{token}")


auth = Authorization()
print(auth.authorization({"name": "test_user"}).json())

print(BaseAPI.token)

print(auth.is_alive(BaseAPI.token).text)