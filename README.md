# Платформа для самообучения студентов

Платформа для самообучения студентов с функционалом управления курсами, материалами и тестирования знаний.

## Технологии

- **Django 4.2.7** - веб-фреймворк
- **Django REST Framework** - REST API
- **JWT (djangorestframework-simplejwt)** - аутентификация
- **SQLite** - база данных (по умолчанию)

## Быстрый старт

См. [QUICKSTART.md](QUICKSTART.md) для подробных инструкций по установке и запуску.

Для настройки проекта на GitHub см. [GITHUB_SETUP.md](GITHUB_SETUP.md)

## Возможности

- **Авторизация и аутентификация**: Регистрация и вход пользователей с использованием JWT токенов
- **Управление контентом**: CRUD операции для разделов и материалов через Django admin и REST API
- **Тестирование знаний**: Функционал тестов для материалов с проверкой ответов
- **Система ролей**: 
  - **Администраторы**: полный доступ ко всем функциям
  - **Преподаватели**: управление своими курсами, материалами и тестами
  - **Студенты**: просмотр материалов и прохождение тестов

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

4. Запустите сервер:
```bash
python manage.py runserver
```

## API Endpoints

### Аутентификация
- `POST /api/auth/login/` - Вход (получение JWT токенов)
- `POST /api/auth/refresh/` - Обновление токена
- `POST /api/users/register/` - Регистрация нового пользователя

### Пользователи
- `GET /api/users/` - Список пользователей (только для администраторов)
- `GET /api/users/me/` - Информация о текущем пользователе
- `GET /api/users/{id}/` - Детали пользователя

### Разделы
- `GET /api/sections/` - Список разделов
- `POST /api/sections/` - Создание раздела (преподаватели)
- `GET /api/sections/{id}/` - Детали раздела
- `PUT /api/sections/{id}/` - Обновление раздела (владелец)
- `DELETE /api/sections/{id}/` - Удаление раздела (владелец)

### Материалы
- `GET /api/materials/` - Список материалов
- `GET /api/materials/?section={id}` - Материалы раздела
- `POST /api/materials/` - Создание материала (преподаватели)
- `GET /api/materials/{id}/` - Детали материала
- `PUT /api/materials/{id}/` - Обновление материала (владелец)
- `DELETE /api/materials/{id}/` - Удаление материала (владелец)

### Тесты
- `GET /api/tests/` - Список тестов
- `GET /api/tests/?material={id}` - Тесты материала
- `POST /api/tests/` - Создание теста (преподаватели)
- `GET /api/tests/{id}/` - Детали теста
- `POST /api/tests/{id}/submit/` - Прохождение теста (студенты)

### Результаты тестов
- `GET /api/test-results/` - Список результатов
- `GET /api/test-results/?test={id}` - Результаты конкретного теста
- `GET /api/test-results/{id}/` - Детали результата

## Использование API

### Регистрация
```bash
POST /api/users/register/
{
    "username": "student1",
    "email": "student1@example.com",
    "password": "password123",
    "password2": "password123",
    "role": "student"
}
```

### Вход
```bash
POST /api/auth/login/
{
    "username": "student1",
    "password": "password123"
}
```

Ответ:
```json
{
    "refresh": "...",
    "access": "..."
}
```

### Использование токена
Добавьте заголовок в запросы:
```
Authorization: Bearer {access_token}
```

### Прохождение теста
```bash
POST /api/tests/{test_id}/submit/
Authorization: Bearer {access_token}
{
    "answers": [
        {
            "question_id": 1,
            "answer_ids": [1, 2]
        },
        {
            "question_id": 2,
            "answer_ids": [5]
        }
    ]
}
```

## Административная панель

Доступна по адресу `/admin/` после создания суперпользователя.

## Роли пользователей

- **admin**: Полный доступ ко всем функциям
- **teacher**: Может создавать и управлять своими разделами, материалами и тестами
- **student**: Может просматривать опубликованные материалы и проходить тесты
