@echo off
chcp 65001 >nul
echo ========================================
echo Настройка проекта для GitHub
echo ========================================
echo.

echo Шаг 1: Инициализация Git...
if not exist .git (
    git init
) else (
    echo Git уже инициализирован
)

echo.
echo Шаг 2: Настройка пользователя...
git config user.name "Denis"
git config user.email "doboleshev@users.noreply.github.com"

echo.
echo Шаг 3: Добавление файлов...
git add .

echo.
echo Шаг 4: Создание начального коммита...
git commit -m "Initial commit: Django learning platform with DRF, JWT auth, and test system"

echo.
echo Шаг 5: Переименование ветки в main...
git branch -M main

echo.
echo Шаг 6: Настройка remote...
git remote remove origin 2>nul
git remote add origin https://github.com/doboleshev/learning_platform.git

echo.
echo ========================================
echo Настройка завершена!
echo ========================================
echo.
echo ВАЖНО: Сначала создайте репозиторий на GitHub:
echo 1. Перейдите на https://github.com/doboleshev
echo 2. Создайте новый репозиторий с именем: learning_platform
echo 3. НЕ добавляйте README, .gitignore или лицензию
echo.
echo После создания репозитория выполните:
echo git push -u origin main
echo.
pause
