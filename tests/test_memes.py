import pytest
import allure
import logging

from endpoints.baseapi import BaseAPI
from endpoints.authorization import Authorization

# Получаем logger для тестов
logger = logging.getLogger(__name__)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Позитивные сценарии")
@allure.title("Проверка получения токена авторизации")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "authorization", "smoke")
def test_authorization_success(auth_token, check_status_code):
    logger.info("Тест: Проверка получения токена авторизации")
    auth = Authorization()
    response = auth.authorization({"name": "test_user"})
    check_status_code(response, 200)
    response_data = response.json()
    logger.debug(f"Получен ответ авторизации: {response_data}")
    assert "token" in response_data, "Токен должен быть в ответе"
    assert response_data["token"], "Токен не должен быть пустым"
    logger.info(f"Токен успешно получен и валидирован")


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@allure.title("Проверка получения токена авторизации с пустым боди")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "authorization", "validation")
def test_authorization_empty_body(auth_token, check_status_code):
    auth = Authorization()
    response = auth.send_request("POST", "/authorize", json={})
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@allure.title("Проверка получения токена авторизации с пустым именем")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "authorization", "validation")
def test_authorization_empty_name(auth_token, check_status_code):
    auth = Authorization()
    response = auth.send_request("POST", "/authorize", json={"name": ""})
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('value', [123, True, [1, "string"], None, {"test": ["test", "test"]}])
@allure.title("Проверка получения токена авторизации, используя разные типы данных для значения")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "authorization", "validation", "data_types")
def test_authorization_different_types_values(auth_token, value, check_status_code):
    auth = Authorization()
    response = auth.send_request("POST", "/authorize", json={"name": value})
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@allure.title("Проверка получения токена авторизации с дополнительным ключом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "authorization", "validation")
def test_authorization_additional_key(auth_token, check_status_code):
    auth = Authorization()
    response = auth.send_request("POST", "/authorize", json={"name": "test_user", "test": "test"})
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@allure.title("Проверка получения токена авторизации с невалидным названием ключа")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "authorization", "validation")
def test_authorization_invalid_key_name(auth_token, check_status_code):
    auth = Authorization()
    response = auth.send_request("POST", "/authorize", json={"test": "test_user"})
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@allure.title("Проверка получения токена авторизации с невалидным эндпоинтом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "authorization", "endpoint")
def test_authorization_invalid_endpoint(auth_token, check_status_code):
    auth = Authorization()
    response = auth.send_request("POST", "/Authorize", json={"name": "test_user"})
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('r_method', ["GET", "PUT", "PATH", "DELETE", "OPTION"])
@allure.title("Проверка получения токена авторизации с невалидным методом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "authorization", "method")
def test_authorization_invalid_method(auth_token, r_method, check_status_code):
    auth = Authorization()
    response = auth.send_request(r_method, "/authorize", json={"name": "test_user"})
    check_status_code(response, 405)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Позитивные сценарии")
@allure.title("Проверка валидности токена")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "authorization", "smoke")
def test_token_is_alive(auth_token, sample_user_name, check_status_code):
    logger.info(f"Тест: Проверка валидности токена для пользователя '{sample_user_name}'")
    auth = Authorization()
    response = auth.is_alive(auth_token)
    check_status_code(response, 200)
    user_name_from_response = response.text.split()[-1]
    logger.debug(f"Имя пользователя из ответа: {user_name_from_response}")
    assert user_name_from_response == sample_user_name, "Имя пользователя не совпадает"
    logger.info("Токен валиден, имя пользователя совпадает")


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('r_method', ["POST", "PUT", "PATH", "DELETE", "OPTION"])
@allure.title("Проверка валидности токена с невалидным методом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "authorization", "method")
def test_token_is_alive_invalid_method(auth_token, sample_user_name, r_method, check_status_code):
    auth = Authorization()
    token = BaseAPI.token
    response = auth.send_request(r_method, endpoint=f"/authorize/{token}")
    check_status_code(response, 405)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@allure.title("Проверка валидности токена с невалидным эндпоинтом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "authorization", "endpoint")
def test_token_is_alive_invalid_endpoint(auth_token, sample_user_name, check_status_code):
    auth = Authorization()
    token = BaseAPI.token
    response = auth.send_request("GET", endpoint=f"/Authorize/{token}")
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Авторизация")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('value', ["", "aaa", 123, True, [1, "string"], None, {"test": ["test", "test"]}])
@allure.title("Проверка валидности токена с невалидным токеном")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "authorization", "validation")
def test_token_is_alive_invalid_token(auth_token, value, sample_user_name, check_status_code):
    auth = Authorization()
    response = auth.send_request("GET", endpoint=f"/authorize/{value}")
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Позитивные сценарии")
@allure.title("Создание нового мема с валидными данными")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "create", "smoke")
def test_create_meme_success(auth_token, create_meme, sample_meme_payload, check_status_code, delete_meme, sample_user_name):
    logger.info("Тест: Создание нового мема с валидными данными")
    logger.debug(f"Payload для создания мема: {sample_meme_payload}")
    response = create_meme.create_new_meme(sample_meme_payload)
    check_status_code(response, 200)
    response_data = response.json()
    meme_id = response_data.get("id")
    logger.info(f"Мем успешно создан с ID: {meme_id}")
    
    assert "id" in response_data, "В ответе должен быть id мема"
    assert response_data["text"] == sample_meme_payload["text"], "Текст мема должен совпадать"
    assert response_data["url"] == sample_meme_payload["url"], "URL мема должен совпадать"
    assert response_data["tags"] == sample_meme_payload["tags"], "Теги должны совпадать"
    assert response_data["info"] == sample_meme_payload["info"], "Информация должна совпадать"
    assert response_data["updated_by"] == sample_user_name, "Имя должно совпадать"
    logger.debug("Все поля мема успешно проверены")
    
    logger.debug(f"Удаление созданного мема с ID: {meme_id}")
    delete_meme.delete_meme_by_id(meme_id)
    logger.info("Тестовый мем удален")


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Позитивные сценарии")
@allure.title("Создание мема с различными типами данных в tags")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("positive", "create", "data_types")
def test_create_meme_with_different_tag_types(auth_token, create_meme, check_status_code, delete_meme):
    payload = {
        "text": "Test meme with mixed tags",
        "url": "https://example.com/meme.jpg",
        "tags": ["string", 123, True],
        "info": {"key": "value"}
    }
    response = create_meme.create_new_meme(payload)
    check_status_code(response, 200)
    meme_id = response.json()["id"]
    delete_meme.delete_meme_by_id(meme_id)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Негативные сценарии")
@allure.title("Создание мема без обязательных ключей: text, url, tags, info")
@pytest.mark.parametrize('missing_field', ["text", "url", "tags", "info"])
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "create", "validation")
def test_create_meme_missing_key(missing_field, auth_token, create_meme, check_status_code):
    payload = {
        "text": "Test meme text",
        "url": "https://example.com/meme.jpg",
        "tags": ["funny", "test"],
        "info": {"colors": ["red", "blue"], "objects": ["text", "image"]}
    }
    payload.pop(missing_field)
    response = create_meme.create_new_meme(payload)
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize("key,empty_value", [("text", ""), ("url", ""), ("tags", []), ("info", {}),],)
@allure.title("Создание мема с пустыми значениями")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "create", "validation")
def test_create_meme_with_empty_fields(auth_token, key, empty_value, create_meme, check_status_code):
    payload = {
        "text": "Test meme text",
        "url": "https://example.com/meme.jpg",
        "tags": ["funny", "test"],
        "info": {"key": "value"}
    }
    payload[key] = empty_value
    response = create_meme.create_new_meme(payload)
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('body', [
    {"text": 123, "url": True, "tags": {"test": ["test", "test"]}, "info": None} ,
    {"text": None, "url": 123, "tags": True, "info": "test"},
    {"text": ["New object3"], "url": None, "tags": 123, "info": True},
    {"text": {"test": ["test", "test"]}, "url": ["New object3"], "tags": None, "info": 123},
    {"text": True, "url": {"test": ["test", "test"]}, "tags": "test", "info": ["New object3"]},])
@allure.title("Создание мема с разными типами данных")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "create", "validation", "data_types")
def test_create_meme_with_different_type_values(auth_token, body, create_meme, check_status_code):
    response = create_meme.create_new_meme(body)
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Негативные сценарии")
@allure.title("Создание мема со всеми пустыми значениями одновремененно")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "create", "validation")
def test_all_fields_empty(auth_token, create_meme, check_status_code):
    payload = {
        "text": "",
        "url": "",
        "tags": [],
        "info": {}
    }
    response = create_meme.create_new_meme(payload)
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Негативные сценарии")
@allure.title("Создание мема c дополнительным ключом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "create", "validation")
def test_create_meme_additional_key(auth_token, create_meme, check_status_code):
    payload = {
        "text": "Test meme text",
        "url": "https://example.com/meme.jpg",
        "tags": ["funny", "test"],
        "info": {"colors": ["red", "blue"], "objects": ["text", "image"]},
        "test": "test"
    }
    response = create_meme.create_new_meme(payload)
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Негативные сценарии")
@allure.title("Создание мема по невалидному эндпоинту")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "create", "endpoint")
def test_create_meme_invalid_endpoint(auth_token, create_meme, check_status_code, sample_meme_payload):
    response = create_meme.send_request(method="POST", endpoint="/Meme", json=sample_meme_payload)
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Негативные сценарии")
@allure.title("Создание мема с пустым телом запроса")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "create", "validation")
def test_create_meme_empty_payload(auth_token, create_meme, check_status_code):
    response = create_meme.create_new_meme({})
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Создание мемов")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('r_method', ["PUT", "PATCH", "DELETE", "OPTION"])
@allure.title("Создание мема с невалидным HTTP методом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "create", "method")
def test_create_meme_invalid_method(auth_token, create_meme, sample_meme_payload, r_method, check_status_code):
    response = create_meme.send_request(method=r_method, endpoint="/meme", json=sample_meme_payload)
    check_status_code(response, 405)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Получение мемов")
@allure.story("Позитивные сценарии")
@allure.title("Получение списка всех мемов")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "get", "smoke")
def test_get_all_memes(auth_token, get_meme, check_status_code):
    logger.info("Тест: Получение списка всех мемов")
    response = get_meme.get_all_memes_endpoint()
    check_status_code(response, 200)
    memes_list = response.json()
    logger.info(f"Получено мемов: {len(memes_list) if isinstance(memes_list, list) else 'N/A'}")
    assert memes_list is not None
    logger.debug(f"Список мемов получен успешно")


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Получение мемов")
@allure.story("Позитивные сценарии")
@allure.title("Получение мема по существующему id")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "get", "smoke")
def test_get_meme_by_id_success(auth_token, get_meme, created_meme_id, check_status_code, sample_user_name):
    logger.info(f"Тест: Получение мема по ID: {created_meme_id}")
    response = get_meme.get_meme_by_id_endpoint(created_meme_id)
    check_status_code(response, 200)
    response_data = response.json()
    logger.debug(f"Полученные данные мема: ID={response_data.get('id')}, Text={response_data.get('text')[:50]}...")
    assert response_data["id"] == created_meme_id, "ID мема должен совпадать"
    assert response_data["updated_by"] == sample_user_name, "Имя должно совпадать"
    logger.info("Мем успешно получен, данные валидированы")


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Получение мемов")
@allure.story("Негативные сценарии")
@allure.title("Получение мема по несуществующему id")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "get", "not_found")
def test_get_meme_by_id_not_found(auth_token, get_meme, created_meme_id, check_status_code):
    response = get_meme.get_meme_by_id_endpoint(created_meme_id + 1)
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Получение мемов")
@allure.story("Негативные сценарии")
@allure.title("Получение мемов по невалидному эндпоинту")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "get", "endpoint")
def test_get_meme_invalid_endpoint(auth_token, get_meme, check_status_code):
    response = get_meme.send_request(method="GET", endpoint="/Meme")
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Получение мемов")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('r_method', ["PUT", "PATCH", "DELETE", "OPTION"])
@allure.title("Получение списка мемов с невалидным HTTP методом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "get", "method")
def test_get_all_memes_invalid_method(auth_token, get_meme, r_method, check_status_code):
    response = get_meme.send_request(method=r_method, endpoint="/meme")
    check_status_code(response, 405)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Получение мемов")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('r_method', ["POST", "PATCH", "OPTION"])
@allure.title("Получение мема по ID с невалидным HTTP методом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "get", "method")
def test_get_meme_by_id_invalid_method(auth_token, get_meme, created_meme_id, r_method, check_status_code):
    response = get_meme.send_request(method=r_method, endpoint=f"/meme/{created_meme_id}")
    check_status_code(response, 405)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Обновление мемов")
@allure.story("Позитивные сценарии")
@allure.title("Обновление существующего мема")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "update", "smoke")
def test_update_meme_success(auth_token, update_meme, created_meme_id, check_status_code, sample_user_name):
    logger.info(f"Тест: Обновление мема с ID: {created_meme_id}")
    updated_payload = {
        "id": created_meme_id,
        "text": "Updated meme text",
        "url": "https://example.com/updated_meme.jpg",
        "tags": ["updated", "test"],
        "info": {
            "colors": ["yellow", "green"],
            "objects": ["updated_image"]
        }
    }
    logger.debug(f"Payload для обновления: {updated_payload}")
    response = update_meme.update_meme_endpoint(created_meme_id, updated_payload)
    check_status_code(response, 200)
    response_data = response.json()
    logger.info(f"Мем успешно обновлен. Новый текст: {response_data.get('text')}")
    
    assert response_data["text"] == updated_payload["text"], "Текст должен быть обновлен"
    assert response_data["url"] == updated_payload["url"], "URL должен быть обновлен"
    assert response_data["tags"] == updated_payload["tags"], "Теги должны быть обновлены"
    assert response_data["info"] == updated_payload["info"], "Информация должна быть обновлена"
    assert response_data["updated_by"] == sample_user_name, "Имя должно совпадать"
    logger.debug("Все поля мема успешно обновлены и проверены")


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Обновление мемов")
@allure.story("Позитивные сценарии")
@pytest.mark.parametrize("field,value", [
        ("text", "Updated text 1"),
        ("url", "https://example.com/updated1.jpg"),
        ("tags", ["tag1", "tag2"]),
        ("info", {"colors": ["black"], "objects": ["circle"]}),])
@allure.title("Обновление существующего мема — изменение одного поля")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("positive", "update")
def test_update_one_field(auth_token, update_meme, created_meme_id, check_status_code, sample_user_name, field, value):
    updated_payload = {
        "id": created_meme_id,
        "text": "Updated meme text",
        "url": "https://example.com/updated_meme.jpg",
        "tags": ["updated", "test"],
        "info": {
            "colors": ["yellow", "green"],
            "objects": ["updated_image"]
        }
    }
    updated_payload[field] = value
    response = update_meme.update_meme_endpoint(created_meme_id, updated_payload)
    check_status_code(response, 200)
    response_data = response.json()
    assert response_data[field] == value, f"Поле '{field}' должно быть обновлено"
    for key in updated_payload:
        if key not in (field, "id"):
            assert response_data[key] == updated_payload[key], f"Поле '{key}' не должно меняться"
    assert response_data["updated_by"] == sample_user_name, "Имя должно совпадать"


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Обновление мемов")
@allure.story("Негативные сценарии")
@allure.title("Обновление мема без обязательных полей: id, text, url, tags, info")
@pytest.mark.parametrize('missing_field', ["id", "text", "url", "tags", "info"])
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "update", "validation")
def test_update_meme_missing_fields(missing_field, auth_token, update_meme, created_meme_id, check_status_code):
    payload = {
        "id": created_meme_id,
        "text": "Test meme text",
        "url": "https://example.com/meme.jpg",
        "tags": ["funny", "test"],
        "info": {"colors": ["red", "blue"], "objects": ["text", "image"]}
    }
    payload.pop(missing_field)
    response = update_meme.update_meme_endpoint(created_meme_id, payload)
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Обновление мемов")
@allure.story("Негативные сценарии")
@allure.title("Обновление несуществующего мема")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "update", "not_found")
def test_update_meme_not_found(auth_token, update_meme, created_meme_id, check_status_code):
    payload = {
        "id": created_meme_id,
        "text": "Updated text",
        "url": "https://example.com/meme.jpg",
        "tags": ["test"],
        "info": {"key": "value"}
    }
    response = update_meme.update_meme_endpoint(created_meme_id + 1, payload)
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Обновление мемов")
@allure.story("Негативные сценарии")
@allure.title("Обновление мема с несовпадающим id в URL и payload")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "update", "validation")
def test_update_meme_id_mismatch(auth_token, update_meme, created_meme_id, check_status_code):
    payload = {
        "id": created_meme_id,
        "text": "Updated text",
        "url": "https://example.com/meme.jpg",
        "tags": ["test"],
        "info": {"key": "value"}
    }
    response = update_meme.update_meme_endpoint(1, payload)
    check_status_code(response, 403)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Обновление мемов")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize("key,empty_value", [("text", ""), ("url", ""), ("tags", []), ("info", {})])
@allure.title("Обновление мема с пустыми значениями")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "update", "validation")
def test_update_meme_with_empty_fields(auth_token, update_meme, created_meme_id, key, empty_value, check_status_code):
    payload = {
        "id": created_meme_id,
        "text": "Test meme text",
        "url": "https://example.com/meme.jpg",
        "tags": ["funny", "test"],
        "info": {"colors": ["red", "blue"], "objects": ["text", "image"]}
    }
    payload[key] = empty_value
    response = update_meme.update_meme_endpoint(created_meme_id, payload)
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Обновление мемов")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('body', [
    {"id": None, "text": 123, "url": True, "tags": {"test": ["test", "test"]}, "info": None},
    {"id": None, "text": None, "url": 123, "tags": True, "info": "test"},
    {"id": None, "text": ["New object3"], "url": None, "tags": 123, "info": True},
    {"id": None, "text": {"test": ["test", "test"]}, "url": ["New object3"], "tags": None, "info": 123},
    {"id": None, "text": True, "url": {"test": ["test", "test"]}, "tags": "test", "info": ["New object3"]},
])
@allure.title("Обновление мема с разными типами данных")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "update", "validation", "data_types")
def test_update_meme_with_different_type_values(auth_token, update_meme, created_meme_id, body, check_status_code):
    body["id"] = created_meme_id
    response = update_meme.update_meme_endpoint(created_meme_id, body)
    check_status_code(response, 400)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Обновление мемов")
@allure.story("Негативные сценарии")
@allure.title("Обновление мемов по невалидному эндпоинту")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "update", "endpoint")
def test_update_meme_invalid_endpoint(auth_token, update_meme, check_status_code, created_meme_id):
    response = update_meme.send_request(method="PUT", endpoint=f"/Meme/{created_meme_id}")
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Обновление мемов")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('r_method', ["POST", "PATCH", "OPTION"])
@allure.title("Обновление мема с невалидным HTTP методом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "update", "method")
def test_update_meme_invalid_method(auth_token, update_meme, created_meme_id, sample_meme_payload, r_method, check_status_code):
    payload = {
        "id": created_meme_id,
        "text": sample_meme_payload["text"],
        "url": sample_meme_payload["url"],
        "tags": sample_meme_payload["tags"],
        "info": sample_meme_payload["info"]
    }
    response = update_meme.send_request(method=r_method, endpoint=f"/meme/{created_meme_id}", json=payload)
    check_status_code(response, 405)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Удаление мемов")
@allure.story("Позитивные сценарии")
@allure.title("Удаление существующего мема")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("positive", "delete", "smoke")
def test_delete_meme_success(auth_token, get_meme, created_meme_id, delete_meme, check_status_code):
    logger.info(f"Тест: Удаление мема с ID: {created_meme_id}")
    response = delete_meme.delete_meme_by_id(created_meme_id)
    check_status_code(response, 200)
    logger.info(f"Мем с ID {created_meme_id} успешно удален")
    
    logger.debug("Проверка, что мем действительно удален")
    get_response = get_meme.get_meme_by_id_endpoint(created_meme_id)
    check_status_code(get_response, 404)
    logger.info("Подтверждено: мем не найден после удаления")


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Удаление мемов")
@allure.story("Негативные сценарии")
@allure.title("Удаление несуществующего мема")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("negative", "delete", "not_found")
def test_delete_meme_not_found(auth_token, check_status_code, delete_meme, created_meme_id):
    response = delete_meme.delete_meme_by_id(created_meme_id + 1)
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Удаление мемов")
@allure.story("Негативные сценарии")
@allure.title("Удаление мемов по невалидному эндпоинту")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "delete", "endpoint")
def test_delete_meme_invalid_endpoint(auth_token, delete_meme, check_status_code, created_meme_id):
    response = delete_meme.send_request(method="DELETE", endpoint=f"/Meme/{created_meme_id}")
    check_status_code(response, 404)


@allure.epic("Тестирование эндпоинтов")
@allure.feature("Удаление мемов")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize('r_method', ["POST", "PATCH", "OPTION"])
@allure.title("Удаление мема с невалидным HTTP методом")
@allure.severity(allure.severity_level.MINOR)
@allure.tag("negative", "delete", "method")
def test_delete_meme_invalid_method(auth_token, delete_meme, created_meme_id, r_method, check_status_code):
    response = delete_meme.send_request(method=r_method, endpoint=f"/meme/{created_meme_id}")
    check_status_code(response, 405)


@allure.epic("Интеграционные тесты")
@allure.story("Интеграционные тесты")
@allure.title("Полный цикл: создание, получение, обновление, удаление мема")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("integration", "smoke", "lifecycle")
def test_full_meme_lifecycle(auth_token, sample_meme_payload, create_meme, get_meme, update_meme, delete_meme, check_status_code):
    logger.info("=" * 80)
    logger.info("ИНТЕГРАЦИОННЫЙ ТЕСТ: Полный жизненный цикл мема")
    logger.info("=" * 80)
    
    # Шаг 1: Создание
    logger.info("ШАГ 1: Создание мема")
    create_response = create_meme.create_new_meme(sample_meme_payload)
    check_status_code(create_response, 200)
    meme_id = create_response.json()["id"]
    logger.info(f"✓ Мем создан с ID: {meme_id}")

    # Шаг 2: Получение
    logger.info("ШАГ 2: Получение созданного мема")
    get_response = get_meme.get_meme_by_id_endpoint(meme_id)
    check_status_code(get_response, 200)
    assert get_response.json()["text"] == sample_meme_payload["text"]
    logger.info("✓ Мем успешно получен, данные совпадают")

    # Шаг 3: Обновление
    logger.info("ШАГ 3: Обновление мема")
    updated_payload = {
        "id": meme_id,
        "text": "Lifecycle updated text",
        "url": "https://example.com/lifecycle.jpg",
        "tags": ["lifecycle", "test"],
        "info": {"status": "updated"}
    }
    update_response = update_meme.update_meme_endpoint(meme_id, updated_payload)
    check_status_code(update_response, 200)
    assert update_response.json()["text"] == updated_payload["text"]
    logger.info("✓ Мем успешно обновлен")

    # Шаг 4: Проверка обновления
    logger.info("ШАГ 4: Проверка обновленных данных")
    get_updated_response = get_meme.get_meme_by_id_endpoint(meme_id)
    check_status_code(get_updated_response, 200)
    assert get_updated_response.json()["text"] == updated_payload["text"]
    logger.info("✓ Обновленные данные подтверждены")

    # Шаг 5: Удаление
    logger.info("ШАГ 5: Удаление мема")
    delete_response = delete_meme.delete_meme_by_id(meme_id)
    check_status_code(delete_response, 200)
    logger.info("✓ Мем успешно удален")

    # Шаг 6: Проверка удаления
    logger.info("ШАГ 6: Проверка, что мем удален")
    get_deleted_response = get_meme.get_meme_by_id_endpoint(meme_id)
    check_status_code(get_deleted_response, 404)
    logger.info("✓ Подтверждено: мем не найден")
    logger.info("=" * 80)
    logger.info("ИНТЕГРАЦИОННЫЙ ТЕСТ ЗАВЕРШЕН УСПЕШНО")
    logger.info("=" * 80)
