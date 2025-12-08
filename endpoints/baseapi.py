import requests
import allure
import json
import time
import logging

# Получаем logger для API классов
logger = logging.getLogger(__name__)


class BaseAPI:

    url = "http://memesapi.course.qa-practice.com/"
    response = None
    json_response = None
    token = None

    def send_request(self, method="GET", endpoint="", retries=3, backoff=1, headers=None, **kwargs):
        headers = headers or {}
        full_url = self.url + endpoint

        if BaseAPI.token:
            headers["Authorization"] = f'{BaseAPI.token}'

        # Логирование запроса
        logger.info(f"→ HTTP {method} {full_url}")
        
        # Логирование тела запроса, если есть
        if 'json' in kwargs and kwargs['json']:
            logger.debug(f"Request body: {json.dumps(kwargs['json'], ensure_ascii=False, indent=2)}")
        elif 'data' in kwargs:
            logger.debug(f"Request data: {kwargs['data']}")

        for attempt in range(1, retries + 1):
            try:
                r = requests.request(method, full_url, headers=headers, **kwargs)
                self.response = r

                # Логирование ответа
                logger.info(f"← Response: {r.status_code} {r.reason}")
                
                if 500 <= r.status_code < 600 and attempt < retries:
                    logger.warning(f"[Retry] Ошибка {r.status_code}, попытка {attempt}/{retries}")
                    time.sleep(backoff * attempt)
                    continue

                if "application/json" in r.headers.get("Content-Type", "").lower():
                    try: 
                        self.json_response = r.json()
                        logger.debug(f"Response JSON: {json.dumps(self.json_response, ensure_ascii=False, indent=2)[:500]}...")
                    except ValueError:
                        self.json_response = None
                        logger.error("Ошибка: ответ не является валидным JSON!")
                else:
                    self.json_response = None
                    logger.debug(f"Content-Type не JSON: {r.headers.get('Content-Type', 'unknown')}")

                if self.json_response is not None:
                    allure.attach(
                        json.dumps(self.json_response, indent=2, ensure_ascii=False),
                        name="Response JSON",
                        attachment_type=allure.attachment_type.JSON
                    )
                
                return r

            except (requests.Timeout, requests.ConnectionError) as ex:
                logger.error(f"[Retry] Сетевая ошибка '{ex}', попытка {attempt}/{retries}")
                if attempt < retries: 
                    time.sleep(backoff * attempt)
                else: 
                    raise

        raise Exception("Запрос не удался после всех retry")
