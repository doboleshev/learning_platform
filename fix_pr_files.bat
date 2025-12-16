@echo off
chcp 65001 >nul
echo ========================================
echo Добавление всех файлов проекта в Pull Request
echo ========================================
echo.

echo Проверка текущей ветки...
git branch --show-current

echo.
echo Добавление всех файлов...
git add -A

echo.
echo Статус Git:
git status

echo.
echo Файлы, готовые к коммиту:
git diff --cached --name-only

echo.
echo ========================================
echo Готово!
echo ========================================
echo.
echo Теперь выполните:
echo git commit -m "feat: добавлены все файлы проекта"
echo git push -u origin feature/improvements
echo.
pause
