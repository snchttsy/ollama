import os
import re
import requests

# Путь к результатам Marker
BASE_DIR = r"C:\Users\snchttsy\Ollama\marker\conversion_results"

# Путь для сохранения выжимок
OUTPUT_DIR = r"C:\Users\snchttsy\Ollama\summaries"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Модель Ollama
OLLAMA_MODEL = "rev"  # кастомная модель на основе mistral:7b


# --- Markdown extractor ---
def extract_text(folder_path: str) -> str:
    full_text = ""

    # ищем .md файл
    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            md_path = os.path.join(folder_path, file)
            with open(md_path, "r", encoding="utf-8") as f:
                full_text += f.read()
            break

    return full_text


# --- Генерация через Ollama ---
def generate_summary(text: str) -> str:
    prompt = f"{text}\n\nСделай резюме строго по шаблону."

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code == 200:
        return response.json().get("response", "").strip()
    else:
        print(f"Ошибка Ollama: {response.status_code} — {response.text}")
        return ""


# --- Постобработка ---
def postprocess_summary(summary: str) -> str:
    # убираем блоки кода
    summary = re.sub(r"```.*?```", "", summary, flags=re.S)

    # нормализуем пустые строки
    summary = re.sub(r"\n{3,}", "\n\n", summary).strip()

    # обязательные секции
    sections = {
        "## Цели исследования": "Не указано.",
        "## Методы и ход работы": "Не указано.",
        "## Результаты и выводы": "Не указано.",
        "## Авторы и области исследований": "Не указано."
    }
    for sec, default_text in sections.items():
        if sec not in summary:
            summary += f"\n\n{sec}\n{default_text}"

    return summary


# --- Основной цикл ---
for folder_name in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, folder_name)
    if os.path.isdir(folder_path):
        print(f"Обработка: {folder_name}")
        text = extract_text(folder_path)

        if not text.strip():
            print("Нет текста для обработки.")
            continue

        raw_summary = generate_summary(text)
        clean_summary = postprocess_summary(raw_summary)

        output_file = os.path.join(OUTPUT_DIR, folder_name + "_summary.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(clean_summary)

        print(f"Сохранено: {output_file}")
