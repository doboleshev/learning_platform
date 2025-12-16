# Инструкции по запуску проекта

Из-за проблем с кодировкой в PowerShell при работе с кириллицей в пути, выполните следующие команды вручную:

## Вариант 1: Использование скрипта

Дважды кликните на файл `run_migrations.bat` - он выполнит миграции автоматически.

## Вариант 2: Ручное выполнение команд

Откройте командную строку (cmd) или PowerShell и выполните:

```cmd
cd C:\Users\Денис\learning_platform
python manage.py makemigrations
python manage.py migrate
```

## Вариант 3: Использование Python напрямую

Если у вас проблемы с путем, используйте полный путь:

```cmd
python "C:\Users\Денис\learning_platform\manage.py" makemigrations
python "C:\Users\Денис\learning_platform\manage.py" migrate
```

## После выполнения миграций

1. Создайте суперпользователя:
```cmd
python "C:\Users\Денис\learning_platform\manage.py" createsuperuser
```

2. Или создайте тестовых пользователей:
```cmd
python "C:\Users\Денис\learning_platform\setup.py"
```

3. Запустите сервер:
```cmd
python "C:\Users\Денис\learning_platform\manage.py" runserver
```

## Альтернативное решение

Если проблемы с кодировкой продолжаются, рекомендуется:

1. Переместить проект в директорию без кириллицы, например:
   - `C:\Projects\learning_platform`
   - `C:\dev\learning_platform`

2. Или использовать виртуальное окружение и работать из него.
