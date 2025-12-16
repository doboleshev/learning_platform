# Быстрый старт: Загрузка проекта на GitHub

## Шаг 1: Создайте репозиторий на GitHub

1. Перейдите на https://github.com/doboleshev
2. Нажмите зеленую кнопку "New" или "+" → "New repository"
3. **Название:** `learning_platform`
4. **Описание:** "Платформа для самообучения студентов на Django с DRF"
5. Выберите **Public** или **Private**
6. **ВАЖНО:** НЕ ставьте галочки на:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
7. Нажмите **"Create repository"**

## Шаг 2: Настройте Git в проекте

### Вариант A: Использовать BAT файл (Windows)

Дважды кликните на файл `deploy_to_github.bat`

### Вариант B: Использовать Python скрипт

```bash
python setup_git.py
```

### Вариант C: Выполнить команды вручную

Откройте командную строку (cmd) в папке проекта:

```bash
git init
git config user.name "Denis"
git config user.email "doboleshev@users.noreply.github.com"
git add .
git commit -m "Initial commit: Django learning platform with DRF, JWT auth, and test system"
git branch -M main
git remote add origin https://github.com/doboleshev/learning_platform.git
```

## Шаг 3: Отправьте код на GitHub

```bash
git push -u origin main
```

**Если появится запрос на аутентификацию:**
- Используйте **Personal Access Token** вместо пароля
- Создайте токен: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Права: выберите `repo`
- Скопируйте токен и используйте его как пароль

## Шаг 4: Создайте Pull Request

### Создание ветки для изменений

```bash
# Используйте скрипт
python create_pr_branch.py

# Или вручную
git checkout -b feature/improvements
```

### Внесите изменения и отправьте

```bash
# Внесите изменения в код
# ...

# Добавьте изменения
git add .

# Создайте коммит
git commit -m "Описание ваших изменений"

# Отправьте ветку
git push -u origin feature/improvements
```

### Создайте Pull Request на GitHub

1. Перейдите на https://github.com/doboleshev/learning_platform
2. Нажмите **"Compare & pull request"** (появится после push)
3. Заполните:
   - **Title:** Краткое описание изменений
   - **Description:** Детальное описание
4. Нажмите **"Create pull request"**
5. После проверки нажмите **"Merge pull request"**

## Готово! 🎉

Ваш проект теперь на GitHub с возможностью создания Pull Requests.
