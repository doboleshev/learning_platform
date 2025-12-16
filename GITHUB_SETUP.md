# Инструкция по настройке проекта на GitHub

## Шаг 1: Создание репозитория на GitHub

1. Перейдите на https://github.com/doboleshev
2. Нажмите кнопку "New" или "+" → "New repository"
3. Название репозитория: `learning_platform`
4. Описание: "Платформа для самообучения студентов на Django с DRF"
5. Выберите "Public" или "Private"
6. **ВАЖНО:** НЕ добавляйте README, .gitignore или лицензию (они уже есть в проекте)
7. Нажмите "Create repository"

## Шаг 2: Инициализация Git в проекте

Выполните один из вариантов:

### Вариант A: Использовать Python скрипт (рекомендуется)

```bash
python setup_git.py
```

### Вариант B: Выполнить команды вручную

Откройте командную строку (cmd) в папке проекта и выполните:

```bash
# Инициализация Git
git init

# Настройка пользователя (если еще не настроено)
git config user.name "Denis"
git config user.email "doboleshev@users.noreply.github.com"

# Добавление всех файлов
git add .

# Создание начального коммита
git commit -m "Initial commit: Django learning platform with DRF, JWT auth, and test system"

# Переименование ветки в main
git branch -M main

# Добавление remote для GitHub
git remote add origin https://github.com/doboleshev/learning_platform.git
```

## Шаг 3: Отправка кода на GitHub

```bash
git push -u origin main
```

Если появится ошибка аутентификации, используйте Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Создайте новый токен с правами `repo`
3. Используйте токен вместо пароля при push

## Шаг 4: Создание ветки для Pull Request

### Вариант A: Использовать скрипт

```bash
python create_pr_branch.py
```

### Вариант B: Выполнить команды вручную

```bash
# Убедитесь, что вы на ветке main
git checkout main
git pull origin main

# Создайте новую ветку для изменений
git checkout -b feature/improvements

# Внесите изменения в проект
# ...

# Добавьте изменения
git add .

# Создайте коммит
git commit -m "Описание ваших изменений"

# Отправьте ветку на GitHub
git push -u origin feature/improvements
```

## Шаг 5: Создание Pull Request на GitHub

1. Перейдите на https://github.com/doboleshev/learning_platform
2. Вы увидите уведомление о новой ветке с кнопкой "Compare & pull request"
3. Или перейдите в раздел "Pull requests" → "New pull request"
4. Выберите:
   - Base: `main` (ветка, в которую хотите влить изменения)
   - Compare: `feature/improvements` (ваша ветка с изменениями)
5. Заполните описание Pull Request:
   - Заголовок: краткое описание изменений
   - Описание: детальное описание того, что было изменено и зачем
6. Нажмите "Create pull request"
7. После проверки и одобрения (если нужно), нажмите "Merge pull request"

## Полезные команды Git

```bash
# Проверить статус
git status

# Посмотреть историю коммитов
git log --oneline

# Посмотреть все ветки
git branch -a

# Переключиться на другую ветку
git checkout main

# Обновить локальную ветку main
git checkout main
git pull origin main

# Удалить локальную ветку
git branch -d feature/improvements

# Удалить удаленную ветку
git push origin --delete feature/improvements
```

## Структура веток

- `main` - основная ветка с рабочим кодом
- `feature/*` - ветки для новых функций
- `fix/*` - ветки для исправления багов
- `docs/*` - ветки для обновления документации

## Примеры названий веток

- `feature/add-user-profiles` - добавление профилей пользователей
- `feature/improve-test-system` - улучшение системы тестирования
- `fix/login-bug` - исправление бага входа
- `docs/update-readme` - обновление документации
