import requests
import allure
import json
import time


class Endpoint:
    url = "http://memesapi.course.qa-practice.com/"
    response = None
    json_response = None

    def send_request(self, method="GET", endpoint="", retries=3, backoff=1, expected_status=200, **kwargs):
        for attempt in range(1, retries + 1):
            try:
                r = requests.request(method, self.url + endpoint, **kwargs)
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
                    print("Ошибка: Content-Type не JSON!")

                try: assert r.status_code == expected_status, f"Ожидался {expected_status}, получен {r.status_code}"
                except AssertionError as e: print(f"[ASSERT FAILED] {e}")

                if self.json_response is not None:
                    allure.attach(
                        json.dumps(self.json_response, indent=2, ensure_ascii=False),
                        name="Response JSON",
                        attachment_type=allure.attachment_type.JSON
                    )
                allure.attach(
                    f"Status code: {r.status_code}\n\nResponse body:\n{r.text}",
                    name="Response",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                return r

            except (requests.Timeout, requests.ConnectionError) as ex:
                print(f"[Retry] Сетевая ошибка '{ex}', попытка {attempt}/{retries}")
                if attempt < retries: time.sleep(backoff * attempt)
                else: raise

        raise Exception("Запрос не удался после всех retry")