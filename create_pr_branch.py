#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для создания ветки и подготовки к Pull Request
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
    print("Создание ветки для Pull Request")
    print("=" * 60)
    
    # Проверяем, что мы на ветке main
    result = subprocess.run('git branch --show-current', shell=True, capture_output=True, text=True)
    current_branch = result.stdout.strip()
    
    print(f"\nТекущая ветка: {current_branch}")
    
    # Переключаемся на main если нужно
    if current_branch != 'main':
        print(f"\nПереключение на ветку main...")
        run_command('git checkout main', cwd=project_dir)
        run_command('git pull origin main', cwd=project_dir)
    
    # Создаем новую ветку для изменений
    branch_name = input("\nВведите название ветки (например: feature/improvements или fix/bug-fix): ").strip()
    if not branch_name:
        branch_name = "feature/improvements"
    
    print(f"\nСоздание ветки: {branch_name}")
    run_command(f'git checkout -b {branch_name}', cwd=project_dir)
    
    print("\n" + "=" * 60)
    print("Ветка создана!")
    print("=" * 60)
    print(f"\nВы сейчас на ветке: {branch_name}")
    print("\nСледующие шаги:")
    print("1. Внесите необходимые изменения в проект")
    print("2. Добавьте изменения:")
    print("   git add .")
    print("3. Создайте коммит:")
    print("   git commit -m 'Описание ваших изменений'")
    print(f"4. Отправьте ветку на GitHub:")
    print(f"   git push -u origin {branch_name}")
    print("\n5. Затем создайте Pull Request на GitHub:")
    print("   https://github.com/doboleshev/learning_platform/compare")

if __name__ == '__main__':
    main()
