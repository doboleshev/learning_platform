#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для настройки Git репозитория и подготовки к GitHub
"""
import subprocess
import os
import sys

def run_command(cmd, cwd=None):
    """Выполнить команду и вывести результат"""
    print(f"Выполняется: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"Ошибка: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Ошибка выполнения команды: {e}")
        return False

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("=" * 60)
    print("Настройка Git репозитория для проекта")
    print("=" * 60)
    
    # 1. Инициализация Git репозитория
    print("\n1. Инициализация Git репозитория...")
    if not os.path.exists('.git'):
        run_command('git init', cwd=project_dir)
    else:
        print("Git репозиторий уже инициализирован")
    
    # 2. Настройка пользователя (если не настроен)
    print("\n2. Проверка настроек Git...")
    run_command('git config user.name "Denis"', cwd=project_dir)
    run_command('git config user.email "doboleshev@users.noreply.github.com"', cwd=project_dir)
    
    # 3. Добавление всех файлов
    print("\n3. Добавление файлов в Git...")
    run_command('git add .', cwd=project_dir)
    
    # 4. Создание начального коммита
    print("\n4. Создание начального коммита...")
    run_command('git commit -m "Initial commit: Django learning platform with DRF, JWT auth, and test system"', cwd=project_dir)
    
    # 5. Создание основной ветки main
    print("\n5. Создание основной ветки main...")
    run_command('git branch -M main', cwd=project_dir)
    
    # 6. Добавление remote для GitHub
    print("\n6. Настройка remote для GitHub...")
    github_url = "https://github.com/doboleshev/learning_platform.git"
    run_command(f'git remote remove origin', cwd=project_dir)
    run_command(f'git remote add origin {github_url}', cwd=project_dir)
    
    print("\n" + "=" * 60)
    print("Настройка завершена!")
    print("=" * 60)
    print("\nСледующие шаги:")
    print("1. Создайте репозиторий на GitHub: https://github.com/doboleshev")
    print("2. Назовите репозиторий: learning_platform")
    print("3. НЕ инициализируйте его с README, .gitignore или лицензией")
    print("4. После создания репозитория выполните:")
    print(f"   git push -u origin main")
    print("\n5. Для создания pull request:")
    print("   git checkout -b feature/improvements")
    print("   # Внесите изменения")
    print("   git add .")
    print("   git commit -m 'Описание изменений'")
    print("   git push -u origin feature/improvements")
    print("\n6. Затем создайте Pull Request на GitHub")

if __name__ == '__main__':
    main()
