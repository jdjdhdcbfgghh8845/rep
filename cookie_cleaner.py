import os
import psutil
import shutil
import sqlite3
from pathlib import Path

# Список процессов браузеров, которые нужно закрыть для разблокировки файлов
BROWSERS = ["chrome.exe", "msedge.exe", "firefox.exe", "opera.exe", "brave.exe", "vivaldi.exe"]

def kill_browsers():
    """Закрывает запущенные браузеры, чтобы файлы куки не были заняты."""
    print("System response: Закрытие браузеров для разблокировки файлов...")
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() in BROWSERS:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def clean_cookies():
    """Ищет и удаляет файлы Cookies во всех популярных браузерах."""
    user_data = os.environ.get('LOCALAPPDATA')
    roaming_data = os.environ.get('APPDATA')
    
    # Массив путей, где браузеры хранят куки
    paths = [
        # Google Chrome
        Path(user_data) / "Google/Chrome/User Data",
        # Microsoft Edge
        Path(user_data) / "Microsoft/Edge/User Data",
        # Opera / Opera GX
        Path(roaming_data) / "Opera Software/Opera Stable",
        Path(roaming_data) / "Opera Software/Opera GX Stable",
        # Brave
        Path(user_data) / "BraveSoftware/Brave-Browser/User Data",
        # Firefox (профили хранятся в Roaming)
        Path(roaming_data) / "Mozilla/Firefox/Profiles"
    ]

    deleted_count = 0
    
    for base_path in paths:
        if not base_path.exists():
            continue
            
        # Рекурсивный поиск файлов с именем 'Cookies' или 'cookies.sqlite'
        for root, dirs, files in os.walk(base_path):
            for file in files:
                # Chromium браузеры используют 'Cookies', Firefox использует 'cookies.sqlite'
                if file.lower() in ['cookies', 'cookies.sqlite', 'cookies-journal']:
                    target_file = Path(root) / file
                    try:
                        os.remove(target_file)
                        print(f"[УДАЛЕНО] {target_file}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"[ОШИБКА] Не удалось удалить {target_file}: {e}")

    print(f"\nSystem response: Очистка завершена. Удалено файлов: {deleted_count}")

if __name__ == "__main__":
    kill_browsers()
    clean_cookies()
