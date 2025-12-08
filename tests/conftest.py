import pytest
import allure
import json
import requests
import logging
import os
from datetime import datetime
from endpoints.authorization import Authorization
from endpoints.baseapi import BaseAPI
from endpoints.create_meme import CreateMeme
from endpoints.delete_meme import DeleteMeme
from endpoints.get_meme import GetMeme
from endpoints.update_meme import UpdateMeme

# Настройка логирования
def setup_logging():
    """Настройка логирования для тестов"""
    # Создаем директорию для логов, если её нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Имя файла лога с датой и временем
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"test_run_{timestamp}.log")
    
    # Настройка формата логирования
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Настройка root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Очистка существующих обработчиков
    logger.handlers.clear()
    
    # Обработчик для файла
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(log_format, date_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', date_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Логирование для requests (опционально, для отладки HTTP запросов)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    return logger

# Инициализация логирования при импорте модуля
logger = setup_logging()


@pytest.fixture(scope="session")
def sample_user_name():
    user_name = "test_user"
    return user_name


@pytest.fixture(scope="session", autouse=True)
def auth_token(sample_user_name):
    logger.info("=" * 80)
    logger.info("НАЧАЛО ТЕСТОВОЙ СЕССИИ")
    logger.info("=" * 80)
    
    auth = Authorization()

    if BaseAPI.token:
        resp = auth.is_alive(BaseAPI.token)
        if resp.status_code == 200:
            logger.info("Используется существующий валидный токен")
            return BaseAPI.token
    
    logger.info("Получение нового токена авторизации...")
    response = auth.authorization({"name": {sample_user_name}})
    assert response.status_code == 200, "Не удалось получить токен авторизации"
    logger.info(f"Токен успешно получен. Статус: {response.status_code}")
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
    logger.debug("Создание тестового мема для теста...")
    response = create_meme.create_new_meme(sample_meme_payload)
    meme_id = response.json()['id']
    logger.debug(f"Мем создан с ID: {meme_id}")
    yield meme_id
    logger.debug(f"Удаление тестового мема с ID: {meme_id}")
    delete_meme.delete_meme_by_id(meme_id)
    logger.debug(f"Мем с ID {meme_id} успешно удален")


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
        logger.debug(f"Проверка статус кода. Ожидается: {expected_status}, Получен: {response.status_code}")
        logger.debug(f"URL запроса: {response.request.method} {response.request.url}")
        
        if response.request.body:
            try:
                import json
                body = json.loads(response.request.body) if isinstance(response.request.body, (str, bytes)) else response.request.body
                logger.debug(f"Тело запроса: {json.dumps(body, ensure_ascii=False, indent=2)}")
            except:
                logger.debug(f"Тело запроса: {response.request.body}")
        
        assert response.status_code == expected_status, (
            f"Ожидался статус {expected_status}, получен {response.status_code}"
        )
        
        logger.info(f"✓ Статус код корректен: {response.status_code}")

        if response.text:
            logger.debug(f"Тело ответа: {response.text[:500]}...")  # Первые 500 символов
            allure.attach(
                f"Status code: {response.status_code}\n\nResponse body:\n{response.text}",
                name="Response",
                attachment_type=allure.attachment_type.TEXT
            )

    return check


# Pytest hooks для логирования
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для логирования результатов выполнения тестов"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        test_name = item.name
        if rep.outcome == "passed":
            logger.info(f"✓ ТЕСТ ПРОЙДЕН: {test_name}")
        elif rep.outcome == "failed":
            logger.error(f"✗ ТЕСТ ПРОВАЛЕН: {test_name}")
            if rep.longrepr:
                logger.error(f"Ошибка: {rep.longrepr}")
        elif rep.outcome == "skipped":
            logger.warning(f"⊘ ТЕСТ ПРОПУЩЕН: {test_name}")


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Автоматическое логирование информации о тесте"""
    test_name = request.node.name
    logger.info("")
    logger.info("-" * 80)
    logger.info(f"Запуск теста: {test_name}")
    logger.info(f"Файл: {request.node.fspath}")
    
    # Логирование параметров, если тест параметризован
    if hasattr(request.node, 'callspec'):
        params = request.node.callspec.params
        if params:
            logger.info(f"Параметры теста: {params}")
    
    yield
    
    logger.info(f"Завершение теста: {test_name}")
    logger.info("-" * 80)