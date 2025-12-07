# API Testing Project - Memes API

Проект для тестирования API мемов. Проект включает в себя полноценную структуру с классами для каждого эндпоинта и комплексными тестами различных сценариев.

## Структура проекта

```
Testing_API_final_project/
├── endpoints/          # Классы для работы с эндпоинтами API
│   ├── __init__.py
│   ├── baseapi.py      # Базовый класс для всех API запросов
│   ├── authorization.py # Класс для авторизации
│   ├── create_meme.py  # Класс для создания мемов
│   ├── get_meme.py     # Класс для получения мемов
│   ├── update_meme.py  # Класс для обновления мемов
│   └── delete_meme.py  # Класс для удаления мемов
├── tests/              # Тесты
│   ├── __init__.py
│   ├── conftest.py     # Фикстуры pytest (авторизация, фикстуры для API классов, проверки)
│   └── test_memes.py   # Тестовые сценарии
├── venv/               # Виртуальное окружение Python
└── README.md           # Документация
```

## API Endpoints

Базовый URL: `http://memesapi.course.qa-practice.com/`

### Endpoints:

- `POST /authorize` - Авторизация (получение токена)
- `GET /authorize/<token>` - Проверка валидности токена
- `GET /meme` - Получение списка всех мемов
- `GET /meme/<id>` - Получение мема по ID
- `POST /meme` - Создание нового мема
- `PUT /meme/<id>` - Обновление мема
- `DELETE /meme/<id>` - Удаление мема

**Важно:** Все эндпоинты требуют авторизации через заголовок `Authorization` с токеном.

## Установка

1. Создайте виртуальное окружение (если еще не создано):
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install pytest requests allure-pytest
```

### Основные зависимости:
- `pytest` - фреймворк для тестирования
- `requests` - библиотека для HTTP запросов
- `allure-pytest` - интеграция Allure с pytest для генерации отчетов

## Запуск тестов

### Запуск всех тестов:
```bash
pytest tests/test_memes.py -v
```

### Запуск с генерацией Allure отчетов:
```bash
pytest tests/test_memes.py --alluredir=./allure-results
allure serve ./allure-results
```

### Запуск конкретного теста:
```bash
pytest tests/test_memes.py::test_create_meme_success -v
```

### Запуск тестов по категориям (story):
```bash
# Все тесты авторизации
pytest tests/test_memes.py -k "authorization" -v

# Все тесты создания мемов
pytest tests/test_memes.py -k "create" -v
```

## Особенности реализации

1. **Авторизация один раз за сессию**: Токен генерируется один раз при запуске тестовой сессии через фикстуру `auth_token` с `scope="session"` и `autouse=True`. Токен переиспользуется, если он еще валиден (проверяется через `is_alive`).

2. **Независимость тестов**: Каждый тест может выполняться отдельно. Тесты создают необходимые данные через фикстуры (например, `created_meme_id`) и автоматически очищают их после выполнения.

3. **Читаемость тестов**: Тесты написаны максимально понятно, с использованием Allure декораторов для улучшения отчетности.

4. **Комплексное тестирование**: Тесты покрывают различные сценарии:
   - Успешные операции (200)
   - Ошибки валидации (400) - отсутствие обязательных полей
   - Ошибки 404 - несуществующие ресурсы
   - Ошибки 403 - несовпадение ID в URL и payload
   - Интеграционные сценарии (полный жизненный цикл: создание → получение → обновление → удаление)

5. **Классы для каждого эндпоинта**: Каждый эндпоинт имеет свой класс в папке `endpoints/`, наследующийся от `BaseAPI`.

6. **Retry механизм**: Базовый класс `BaseAPI` включает механизм повторных попыток для сетевых ошибок и ошибок сервера (5xx).

7. **Allure интеграция**: Все тесты используют Allure для генерации подробных отчетов с прикрепленными запросами и ответами.

## Тестовые сценарии

Проект включает следующие группы тестов (всего 20+ тестов):

### Авторизация
- Получение токена авторизации
- Проверка валидности токена

### Создание мемов
- Создание мема с валидными данными
- Создание мема без обязательных полей (text, url, tags, info) - параметризованный тест
- Создание мема с различными типами данных в tags (string, int, bool)
- Создание мема с пустым массивом tags
- Создание мема с пустым телом запроса

### Получение мемов
- Получение списка всех мемов
- Получение мема по существующему ID
- Получение мема по несуществующему ID (404)

### Обновление мемов
- Обновление существующего мема
- Обновление мема без обязательных полей (id, text, url, tags, info) - параметризованный тест
- Обновление несуществующего мема (404)
- Обновление мема с несовпадающим ID в URL и payload (403)

### Удаление мемов
- Удаление существующего мема
- Удаление несуществующего мема (404)

### Интеграционные тесты
- Полный жизненный цикл: создание → получение → обновление → удаление мема

## Использование

### Пример использования API классов:

```python
from endpoints.authorization import Authorization
from endpoints.create_meme import CreateMeme
from endpoints.get_meme import GetMeme
from endpoints.update_meme import UpdateMeme
from endpoints.delete_meme import DeleteMeme

# Авторизация (токен сохраняется в BaseAPI.token)
auth = Authorization()
auth.authorization({"name": "test_user"})

# Создание мема
create_api = CreateMeme()
payload = {
    "text": "Test meme",
    "url": "https://example.com/meme.jpg",
    "tags": ["funny"],
    "info": {"key": "value"}
}
response = create_api.create_new_meme(payload)
meme_id = response.json()["id"]

# Получение мема
get_api = GetMeme()
meme = get_api.get_meme_by_id(meme_id)

# Обновление мема
update_api = UpdateMeme()
updated_payload = {
    "id": meme_id,
    "text": "Updated text",
    "url": "https://example.com/updated.jpg",
    "tags": ["funny", "updated"],
    "info": {"key": "new_value"}
}
update_api.update_meme(meme_id, updated_payload)

# Удаление мема
delete_api = DeleteMeme()
delete_api.delete_meme_by_id(meme_id)
```

## Формат данных мема

Мем должен содержать следующие обязательные поля:

```json
{
    "text": "string",           // Текст мема
    "url": "string",            // URL изображения
    "tags": ["string"],         // Массив тегов (может быть пустым)
    "info": {                   // Дополнительная информация (объект)
        "key": "value"
    }
}
```

При обновлении мема также требуется поле `id` в payload.

## Технические детали

- **Базовый URL**: `http://memesapi.course.qa-practice.com/`
- **Авторизация**: Токен передается в заголовке `Authorization`
- **Формат ответов**: JSON
- **Коды ответов**: 200 (успех), 400 (ошибка валидации), 403 (запрещено), 404 (не найдено)
