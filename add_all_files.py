#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для добавления всех файлов проекта в Git
"""
import subprocess
import os

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
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("=" * 60)
    print("Добавление всех файлов проекта в Git")
    print("=" * 60)
    
    # Проверяем текущую ветку
    result = subprocess.run('git branch --show-current', shell=True, capture_output=True, text=True)
    current_branch = result.stdout.strip()
    print(f"\nТекущая ветка: {current_branch}")
    
    # Добавляем все файлы
    print("\nДобавление всех файлов...")
    run_command('git add .', cwd=project_dir)
    
    # Проверяем статус
    print("\nСтатус Git:")
    run_command('git status', cwd=project_dir)
    
    # Показываем, что будет закоммичено
    print("\nФайлы, готовые к коммиту:")
    run_command('git diff --cached --name-only', cwd=project_dir)
    
    print("\n" + "=" * 60)
    print("Готово! Теперь выполните:")
    print("=" * 60)
    print("git commit -m 'feat: добавлены все файлы проекта'")
    print(f"git push -u origin {current_branch}")

if __name__ == '__main__':
    main()
