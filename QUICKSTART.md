# Быстрый старт

## Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 2: Выполнение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

## Шаг 3: Создание суперпользователя

```bash
python manage.py createsuperuser
```

Или создайте тестовых пользователей:

```bash
python setup.py
```

Это создаст:
- Администратор: `admin` / `admin123`
- Преподаватель: `teacher1` / `teacher123`
- Студент: `student1` / `student123`

## Шаг 4: Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000/

## Шаг 5: Тестирование API

### Регистрация пользователя

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "password2": "password123",
    "role": "student"
  }'
```

### Вход в систему

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "student123"
  }'
```

Ответ будет содержать `access` и `refresh` токены.

### Использование токена

```bash
curl -X GET http://127.0.0.1:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Административная панель

Откройте http://127.0.0.1:8000/admin/ и войдите с учетными данными суперпользователя.

## Примеры работы с API

### Создание раздела (преподаватель)

```bash
curl -X POST http://127.0.0.1:8000/api/sections/ \
  -H "Authorization: Bearer TEACHER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Основы Python",
    "description": "Введение в программирование на Python",
    "is_published": true
  }'
```

### Создание материала

```bash
curl -X POST http://127.0.0.1:8000/api/materials/ \
  -H "Authorization: Bearer TEACHER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Переменные и типы данных",
    "content": "В Python есть несколько типов данных...",
    "section": 1,
    "order": 1,
    "is_published": true
  }'
```

### Создание теста

```bash
curl -X POST http://127.0.0.1:8000/api/tests/ \
  -H "Authorization: Bearer TEACHER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Тест по переменным",
    "description": "Проверка знаний о переменных",
    "material": 1,
    "passing_score": 60
  }'
```

### Прохождение теста (студент)

```bash
curl -X POST http://127.0.0.1:8000/api/tests/1/submit/ \
  -H "Authorization: Bearer STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {
        "question_id": 1,
        "answer_ids": [1]
      },
      {
        "question_id": 2,
        "answer_ids": [3, 4]
      }
    ]
  }'
```
