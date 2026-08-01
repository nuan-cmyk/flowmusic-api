# FlowMusic API (Unofficial Python Client) 🎶🚀

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Неофициальный Python-клиент для [Flow Music](https://www.flowmusic.app/). Позволяет программно генерировать музыку (в том числе на основе загруженных изображений), проверять баланс кредитов и получать данные профиля. Библиотека использует Pydantic для строгой типизации данных и поддерживает SSE-стриминг для отслеживания статуса генерации треков в реальном времени.

## ✨ Основные возможности
- **Генерация музыки:** создание треков по текстовому промпту.
- **Поддержка изображений:** загрузка фото для генерации музыки на основе визуального контента.
- **Выбор модели:** поддержка быстрого режима (`fast`) и выбора конкретного движка (например, `Lyria 3.5`).
- **Управление кредитами:** просмотр реального доступного баланса кредитов.
- **Профиль:** получение данных о пользователе, уровне и истории.
- **Объектно-ориентированная структура:** удобный клиент и строгая типизация ответов с помощью Pydantic.

---

## 📦 Установка

Поскольку библиотека пока не опубликована в PyPI, вы можете установить её напрямую из GitHub:

```bash
pip install git+https://github.com/nuan-cmyk/flowmusic-api.git
```

**Зависимости:**
- `requests`
- `pydantic`
- `sseclient-py`

---

## 🚀 Быстрый старт

### 1. Получение токена авторизации
Для работы с API вам понадобится ваш личный JWT токен. Вот пошаговая инструкция, как его достать:

1. Откройте сайт [flowmusic.app](https://www.flowmusic.app/) в браузере (например, Chrome) и войдите в свой аккаунт.
2. Нажмите **F12**, чтобы открыть панель разработчика (DevTools).
3. Перейдите на вкладку **Network** (Сеть).
4. Обязательно включите фильтр **Fetch/XHR** (чтобы не искать среди картинок и скриптов).
5. Обновите страницу (F5) или сделайте любое действие на сайте (например, откройте свой профиль).
6. В появившемся списке запросов найдите любой запрос, который начинается с `__api/` (например, `level`, `credits` или `me`). Кликните по нему.
7. Справа откроется панель с деталями. Перейдите во вкладку **Headers** (Заголовки), прокрутите вниз до раздела **Request Headers** (Заголовки запроса).
8. Найдите строку `Authorization`. Она будет выглядеть так: `Bearer eyJhbGciOiJIUzI1NiIs...`
9. Скопируйте **весь текст** после слова `Bearer ` (начиная с `eyJ...`). Это и есть ваш токен!

### 2. Проверка баланса

```python
from flowmusic import FlowMusicClient

TOKEN = "ВАШ_JWT_ТОКЕН"

def main():
    client = FlowMusicClient(TOKEN)
    
    # Получаем информацию о пользователе
    me = client.users.get_me()
    print(f"User: {me.username} (ID: {me.id})")
    
    # Проверяем текущий баланс кредитов
    credits = client.billing.get_total_credits()
    print(f"Total Credits: {credits}")

if __name__ == "__main__":
    main()
```

### 3. Генерация трека (с использованием картинки и быстрой модели)

```python
from flowmusic import FlowMusicClient

TOKEN = "ВАШ_JWT_ТОКЕН"
client = FlowMusicClient(TOKEN)

try:
    print("Отправка запроса на генерацию...")
    clips = client.generation.generate_music(
        prompt="Create a fast breakcore track with intense amen breaks and glitchy synth leads",
        # image_path="path/to/your/image.jpg", # Раскомментируйте для генерации по фото
        model="producer:fast",                 # Быстрый режим продюсера
        mode="fast",                           
        selected_model="Lyria 3.5",            # Использование конкретной модели
        timeout=180,                           # Таймаут ожидания (сек)
        poll_interval=5                        # Интервал поллинга готовности
    )
    
    print(f"\nУспешно сгенерировано {len(clips)} трека(ов)!")
    for i, clip in enumerate(clips, 1):
        print(f"\n--- Трек {i} ---")
        print(f"ID: {clip.id}")
        print(f"Title: {clip.title}")
        print(f"Audio URL: {clip.audio_url}")
        print(f"Video URL: {clip.video_url}")

except Exception as e:
    print(f"Ошибка при генерации: {e}")
```

---

## 📂 Структура проекта
```text
flowmusicapi/
├── flowmusic/
│   ├── client.py             # Главный клиент (FlowMusicClient)
│   ├── models/               # Pydantic модели (User, Clip, Billing)
│   └── api/                  # Модули API
│       ├── generation_api.py # Генерация и загрузка изображений
│       ├── billing_api.py    # Баланс кредитов
│       ├── personalize_api.py# Уровень и скоринг
│       └── user_api.py       # Данные пользователя
├── examples/                 # Примеры использования библиотеки
└── setup.py                  # Установочный скрипт
```

---

*Этот проект не аффилирован с официальной командой Flow Music. Используйте на свой страх и риск.*
