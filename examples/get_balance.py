import os
import sys

# Добавляем родительскую папку в sys.path, чтобы можно было импортировать flowmusic без установки
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flowmusic import FlowMusicClient

# Замените на ваш актуальный токен
TOKEN = "YOUR_JWT_TOKEN_HERE"

def main():
    client = FlowMusicClient(TOKEN)
    
    # 1. Получаем информацию о пользователе
    me = client.users.get_me()
    print("User Info:")
    if me:
        print(f"  Name: {me.username}")
        print(f"  ID: {me.user_id}")
    
    # 2. Получаем уровень пользователя
    level = client.personalize.get_level()
    print(f"\nLevel: {level.level} (Upgraded: {level.upgraded})")
    
    # 3. Баланс кредитов
    credits = client.billing.get_total_credits()
    print(f"\nTotal Credits: {credits}")

if __name__ == "__main__":
    main()
