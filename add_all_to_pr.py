#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для добавления ВСЕХ файлов проекта в Pull Request
"""
import subprocess
import os
import glob

def run_command(cmd, cwd=None, capture=False):
    """Выполнить команду"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=capture,
            text=True,
            encoding='utf-8'
        )
        if not capture:
            if result.stdout:
                print(result.stdout)
            if result.stderr and result.returncode != 0:
                print(f"Ошибка: {result.stderr}")
        return result
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("=" * 60)
    print("Добавление ВСЕХ файлов проекта в Pull Request")
    print("=" * 60)
    
    # Проверяем текущую ветку
    result = run_command('git branch --show-current', capture=True)
    current_branch = result.stdout.strip() if result else "unknown"
    print(f"\nТекущая ветка: {current_branch}")
    
    # Проверяем, что в main
    print("\nПроверка файлов в main...")
    run_command('git checkout main', capture=True)
    main_files = run_command('git ls-files', capture=True)
    main_file_count = len(main_files.stdout.strip().split('\n')) if main_files and main_files.stdout else 0
    print(f"Файлов в main: {main_file_count}")
    
    # Возвращаемся на feature ветку
    print(f"\nПереключение на ветку {current_branch}...")
    run_command(f'git checkout {current_branch}')
    
    # Добавляем ВСЕ файлы (включая те, что игнорируются .gitignore, но мы их потом уберем)
    print("\nДобавление всех файлов проекта...")
    
    # Сначала добавляем все файлы, которые не игнорируются
    run_command('git add -A')
    
    # Проверяем статус
    print("\nСтатус Git:")
    run_command('git status')
    
    # Показываем все файлы, которые будут добавлены
    print("\n" + "=" * 60)
    print("Файлы, готовые к коммиту:")
    print("=" * 60)
    result = run_command('git diff --cached --name-only', capture=True)
    if result and result.stdout:
        files = result.stdout.strip().split('\n')
        for i, file in enumerate(files, 1):
            if file:
                print(f"{i}. {file}")
        print(f"\nВсего файлов: {len([f for f in files if f])}")
    
    print("\n" + "=" * 60)
    print("Следующие шаги:")
    print("=" * 60)
    print("1. git commit -m 'feat: добавлены все файлы проекта'")
    print(f"2. git push -u origin {current_branch}")
    print("\nПосле этого все файлы появятся в Pull Request!")

if __name__ == '__main__':
    main()
