import requests
import allure
import json
import time


class BaseAPI:

    url = "http://memesapi.course.qa-practice.com/"
    response = None
    json_response = None
    token = None

    def send_request(self, method="GET", endpoint="", retries=3, backoff=1, headers=None, **kwargs):
        headers = headers or {}

        if BaseAPI.token:
            headers["Authorization"] = f'{BaseAPI.token}'

        for attempt in range(1, retries + 1):
            try:
                r = requests.request(method, self.url + endpoint, headers=headers, **kwargs)
                self.response = r

                if 500 <= r.status_code < 600 and attempt < retries:
                    print(f"[Retry] Ошибка {r.status_code}, попытка {attempt}/{retries}")
                    time.sleep(backoff * attempt)
                    continue

                if "application/json" in r.headers.get("Content-Type", "").lower():
                    try: self.json_response = r.json()
                    except ValueError:
                        self.json_response = None
                        print("Ошибка: ответ не является валидным JSON!")
                else:
                    self.json_response = None
                    print("Content-Type не JSON!")

                if self.json_response is not None:
                    allure.attach(
                        json.dumps(self.json_response, indent=2, ensure_ascii=False),
                        name="Response JSON",
                        attachment_type=allure.attachment_type.JSON
                    )
                
                return r

            except (requests.Timeout, requests.ConnectionError) as ex:
                print(f"[Retry] Сетевая ошибка '{ex}', попытка {attempt}/{retries}")
                if attempt < retries: time.sleep(backoff * attempt)
                else: raise

        raise Exception("Запрос не удался после всех retry")
