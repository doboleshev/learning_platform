# Руководство по внесению изменений

## Создание Pull Request

1. **Создайте ветку для изменений:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
   Или используйте скрипт:
   ```bash
   python create_pr_branch.py
   ```

2. **Внесите изменения в код**

3. **Добавьте изменения:**
   ```bash
   git add .
   ```

4. **Создайте коммит:**
   ```bash
   git commit -m "Описание ваших изменений"
   ```

5. **Отправьте ветку на GitHub:**
   ```bash
   git push -u origin feature/your-feature-name
   ```

6. **Создайте Pull Request на GitHub:**
   - Перейдите на https://github.com/doboleshev/learning_platform
   - Нажмите "Compare & pull request"
   - Заполните описание изменений
   - Нажмите "Create pull request"

## Соглашения о коммитах

Используйте понятные сообщения коммитов:
- `feat: добавлена функция X`
- `fix: исправлена ошибка Y`
- `docs: обновлена документация`
- `refactor: рефакторинг кода`
- `test: добавлены тесты`

## Структура веток

- `main` - основная ветка (всегда стабильна)
- `feature/*` - новые функции
- `fix/*` - исправления багов
- `docs/*` - обновление документации
