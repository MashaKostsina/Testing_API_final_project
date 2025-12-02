import allure
from endpoints.endpoint import Endpoint


class Authorization(Endpoint):
    token = None

    @allure.step("Получение токена авторизации")
    def authorization(self, payload):
        response = self.send_request(method="POST", endpoint="/authorize", json=payload)
        data = response.json()
        token = data.get("token")
        if not token:
            raise Exception("Токен не найден в ответе!")
        Endpoint.token = token
        return response

    @allure.step("Проверка жизни токена")
    def is_alive(self, token):
        return self.send_request(method="GET", endpoint=f"/authorize/{token}")

# auth = Authorization()
# resp = auth.authorization(payload={"name":"qw"})
#
#
# print(resp.text)


