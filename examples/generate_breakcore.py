import os
import sys

# Добавляем родительскую папку в sys.path, чтобы можно было импортировать flowmusic без установки
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flowmusic import FlowMusicClient

# Замените на ваш актуальный токен
TOKEN = "YOUR_JWT_TOKEN_HERE"

def main():
    client = FlowMusicClient(TOKEN)
    
    # Пример генерации музыки с изображением и быстрой моделью
    print("Отправка запроса на генерацию...")
    
    # Можно передать путь к картинке в параметр image_path="path/to/image.jpg"
    # Также можно выбрать модель и режим
    prompt = "Create a fast breakcore track with intense amen breaks and glitchy synth leads"
    
    try:
        clips = client.generation.generate_music(
            prompt=prompt,
            # image_path="path/to/image.png",   # Раскомментируйте и укажите путь, если нужна картинка
            model="producer:fast",              # Используем продюсера 'fast' вместо 'standard'
            mode="fast",                        # Режим 'fast'
            selected_model="Lyria 3.5",         # Можно указать конкретную модель
            timeout=180, 
            poll_interval=5
        )
        
        print(f"\nGenerated {len(clips)} tracks successfully!")
        for i, clip in enumerate(clips, 1):
            print(f"\n--- Track {i} ---")
            print(f"Title: {clip.title}")
            print(f"Tags/Prompt: {clip.operation.sound_prompt}")
            print(f"Audio URL (.m4a): {clip.audio_url}")
            print(f"Audio URL (.wav): {clip.wav_url}")
            print(f"Image URL: {clip.image_url}")
            print(f"Duration: {clip.duration.value}s")
            
    except Exception as e:
        print(f"Failed to generate music: {e}")

if __name__ == "__main__":
    main()
