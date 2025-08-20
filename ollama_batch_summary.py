import os
import requests
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"D:\ollama-1\Tesseract\tesseract.exe"
from PIL import Image

# Путь к результатам Marker
BASE_DIR = r"D:\ollama-1\.venv\Lib\site-packages\conversion_results"
# Путь для сохранения выжимок
OUTPUT_DIR = r"D:\ollama-1\summaries"

# Убедимся, что папка существует
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Задаём модель Ollama
OLLAMA_MODEL = "rev2"

# Функция: объединить текст из .md + OCR с изображений
def extract_text(folder_path):
    md_file = None
    full_text = ""

    # Найдём .md файл
    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            md_file = os.path.join(folder_path, file)
            break

    if md_file:
        with open(md_file, "r", encoding="utf-8") as f:
            full_text += f.read()

    # Добавим текст с изображений
    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith(".jpeg"):
            image_path = os.path.join(folder_path, file)
            try:
                img = Image.open(image_path)
                text = pytesseract.image_to_string(img, lang='rus')
                full_text += "\n\n" + text
            except Exception as e:
                print(f"Ошибка при обработке {image_path}: {e}")

    return full_text

# Функция: отправить текст в Ollama
def generate_summary(text):
    prompt = (
        f"{text}"
    )

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code == 200:
        return response.json().get("response", "").strip()
    else:
        print(f"Ошибка от Ollama: {response.status_code} — {response.text}")
        return None

# Основной цикл по подпапкам
for folder_name in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder_name)
    if os.path.isdir(folder_path):
        print(f"Обработка: {folder_name}")
        text = extract_text(folder_path)
        if not text.strip():
            print("Нет текста для обработки.")
            continue
        summary = generate_summary(text)
        if summary:
            output_file = os.path.join(OUTPUT_DIR, folder_name + "_summary.md")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(summary)
            print(f"Сохранено: {output_file}")
        else:
            print("Ошибка генерации выжимки.")
