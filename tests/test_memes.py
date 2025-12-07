import pytest
import allure
from endpoints.authorization import Authorization



@allure.story("Авторизация")
@allure.title("Проверка получения токена авторизации")
def test_authorization_success(auth_token, check_status_code):
    auth = Authorization()
    response = auth.authorization({"name": "test_user"})
    check_status_code(response, 200)
    assert "token" in response.json(), "Токен должен быть в ответе"
    assert response.json()["token"], "Токен не должен быть пустым"


@allure.story("Авторизация")
@allure.title("Проверка валидности токена")
def test_token_is_alive(auth_token, sample_user_name, check_status_code):
    auth = Authorization()
    response = auth.is_alive(auth_token)
    check_status_code(response, 200)
    assert response.text.split()[-1] == sample_user_name, "Имя пользователя не совпадает"


@allure.story("Получение мемов")
@allure.title("Получение списка всех мемов")
def test_get_all_memes(auth_token, get_meme, check_status_code):
    response = get_meme.get_all_memes_endpoint()
    check_status_code(response, 200)
    print(response.json())
    assert response.json() is not None


@allure.story("Создание мемов")
@allure.title("Создание нового мема с валидными данными")
def test_create_meme_success(auth_token, create_meme, sample_meme_payload, check_status_code, sample_user_name):
    response = create_meme.create_new_meme(sample_meme_payload)
    check_status_code(response, 200)
    response_data = response.json()
    assert "id" in response_data, "В ответе должен быть id мема"
    assert response_data["text"] == sample_meme_payload["text"], "Текст мема должен совпадать"
    assert response_data["url"] == sample_meme_payload["url"], "URL мема должен совпадать"
    assert response_data["tags"] == sample_meme_payload["tags"], "Теги должны совпадать"
    assert response_data["info"] == sample_meme_payload["info"], "Информация должна совпадать"
    assert response_data["updated_by"] ==  sample_user_name, "Имя должно совпадать"


@allure.story("Создание мемов")
@allure.title("Создание мема без обязательных ключей: text, url, tags, info")
@pytest.mark.parametrize('missing_field', ["text", "url", "tags", "info"])
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


@allure.story("Создание мемов")
@allure.title("Создание мема с различными типами данных в tags")
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


@allure.story("Создание мемов")
@allure.title("Создание мема с пустым массивом tags")
def test_create_meme_with_empty_tags(auth_token, create_meme, delete_meme, check_status_code):
    """Тест создания мема с пустым массивом tags"""
    payload = {
        "text": "Test meme",
        "url": "https://example.com/meme.jpg",
        "tags": [],
        "info": {"key": "value"}
    }
    response = create_meme.create_new_meme(payload)
    check_status_code(response, 200)

    meme_id = response.json()["id"]
    delete_meme.delete_meme_by_id(meme_id)


@allure.story("Создание мемов")
@allure.title("Создание мема с пустым телом запроса")
def test_create_meme_empty_payload(auth_token, create_meme, check_status_code):
    response = create_meme.create_new_meme({})
    check_status_code(response, 400)


@allure.story("Получение мемов")
@allure.title("Получение мема по существующему id")
def test_get_meme_by_id_success(auth_token, get_meme, created_meme_id, check_status_code, sample_user_name):
    response = get_meme.get_meme_by_id_endpoint(created_meme_id)
    check_status_code(response, 200)
    response_data = response.json()
    assert response_data["id"] == created_meme_id, "ID мема должен совпадать"
    assert response_data["updated_by"] == sample_user_name, "Имя должно совпадать"


@allure.story("Получение мемов")
@allure.title("Получение мема по несуществующему id")
def test_get_meme_by_id_not_found(auth_token, get_meme, created_meme_id, check_status_code):
    response = get_meme.get_meme_by_id_endpoint(created_meme_id + 1)
    check_status_code(response, 404)


@allure.story("Обновление мемов")
@allure.title("Обновление существующего мема")
def test_update_meme_success(auth_token, create_meme, update_meme, created_meme_id, check_status_code, sample_user_name):
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
    response = update_meme.update_meme_endpoint(created_meme_id, updated_payload)
    check_status_code(response, 200)
    response_data = response.json()
    assert response_data["text"] == updated_payload["text"], "Текст должен быть обновлен"
    assert response_data["url"] == updated_payload["url"], "URL должен быть обновлен"
    assert response_data["tags"] == updated_payload["tags"], "Теги должны быть обновлены"
    assert response_data["info"] == updated_payload["info"], "Информация должна быть обновлена"
    assert response_data["updated_by"] == sample_user_name, "Имя должно совпадать"


@allure.story("Обновление мемов")
@allure.title("Обновление мема без обязательных полей: id, text, url, tags, info")
@pytest.mark.parametrize('missing_field', ["id", "text", "url", "tags", "info"])
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


@allure.story("Обновление мемов")
@allure.title("Обновление несуществующего мема")
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


@allure.story("Обновление мемов")
@allure.title("Обновление мема с несовпадающим id в URL и payload")
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


@allure.story("Удаление мемов")
@allure.title("Удаление существующего мема")
def test_delete_meme_success(auth_token, get_meme, created_meme_id, delete_meme, check_status_code):
    response = delete_meme.delete_meme_by_id(created_meme_id)
    check_status_code(response, 200)
    get_response = get_meme.get_meme_by_id_endpoint(created_meme_id)
    check_status_code(get_response, 404)


@allure.story("Удаление мемов")
@allure.title("Удаление несуществующего мема")
def test_delete_meme_not_found(auth_token, check_status_code, delete_meme, created_meme_id):
    response = delete_meme.delete_meme_by_id(created_meme_id + 1)
    check_status_code(response, 404)


@allure.story("Интеграционные тесты")
@allure.title("Полный цикл: создание, получение, обновление, удаление мема")
def test_full_meme_lifecycle(auth_token, sample_meme_payload, create_meme, get_meme, update_meme, delete_meme, check_status_code):
    create_response = create_meme.create_new_meme(sample_meme_payload)
    check_status_code(create_response, 200)
    meme_id = create_response.json()["id"]

    get_response = get_meme.get_meme_by_id_endpoint(meme_id)
    check_status_code(get_response, 200)
    assert get_response.json()["text"] == sample_meme_payload["text"]

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

    get_updated_response = get_meme.get_meme_by_id_endpoint(meme_id)
    check_status_code(get_updated_response, 200)
    assert get_updated_response.json()["text"] == updated_payload["text"]

    delete_response = delete_meme.delete_meme_by_id(meme_id)
    check_status_code(delete_response, 200)

    get_deleted_response = get_meme.get_meme_by_id_endpoint(meme_id)
    check_status_code(get_deleted_response, 404)





