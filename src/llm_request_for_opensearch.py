import requests

url="http://92.39.53.155:8000/v1/chat/completions"

def request_llm(candidates):

    # system_prompt = (
    #     f"Мне нужно чтобы ты из текста множественных резюме выделил основные данные и выдал ответ в формате JSON без лишней информации"
    #     f"Ответ должен содержать только JSON для вставки в Opensearch"
    #     f'_id = 1'
    #     f'Данные должны начинаться с {{"index": {{"_id": "{"_id"}"}}}}. После первого кандидата должно идти {{"index": {{"_id": "{"_id + 1"}"}}}} _id должен увеличиваться'
    #     f'Не делай перенос строки между кандитатами. JSON должен подходить для вставки в Opensearch'
    # )

    system_prompt = """
Мне нужно чтобы ты из текста множественных резюме выделил основные данные и выдал ответ в формате JSON без лишней информации
Ты парсер резюме. Из текста кандидата ты должен:
1. Самостоятельно определить какие поля есть в тексте
2. Построить подходящую JSON-схему
3. Вернуть ТОЛЬКО валидный JSON объект — без markdown, без пояснений

=== ЖЁСТКИЕ ПРАВИЛА для совместимости с OpenSearch ===

ТИПЫ ДАННЫХ:
- Числа (возраст, стаж, зарплата)  → integer или float, НЕ строки: "age": 26  (не "26")
- Даты                              → формат "YYYY-MM-DD": "applied_at": "2026-04-28"
- Списки навыков, достижений        → массив строк: ["pandas", "scikit-learn"]
- Булевы значения                   → true/false, НЕ строки: "remote_ready": true
- Текстовые поля                    → строка: "name": "Алексей Смирнов"
- Отсутствующие поля                → null для строк, [] для массивов, не пропускай

ЗАПРЕЩЕНО:
- Смешивать типы в одном поле: если поле числовое — всегда число, не строка
- Использовать точки в ключах: НЕ "experience.years" → используй вложенный объект
- Ключи с пробелами или спецсимволами: только snake_case
- Вкладывать массивы в массивы: [["a","b"]] — неверно, только ["a","b"]
- Пустые ключи: "" — недопустимо

ОБЯЗАТЕЛЬНЫЕ ПОЛЯ (должны быть всегда):
- "name"       → string
- "contacts"   данные кандидата для связи
- "status"     → всегда "active"
- "tags"       → массив ключевых слов из резюме


СТРУКТУРА:
- Группируй связанные поля во вложенные объекты: experience{}, skills{}, languages{}
- Называй поля по смыслу на английском в snake_case

Ответ должен содержать только JSON для вставки в Opensearch"
_id = 1
Данные должны начинаться с {"index": {"_id": "1"}} . После первого кандидата должно идти {"index": {"_id": +1}}  _id должен увеличиваться
Не делай перенос строки между кандидатами
Если не хватает информации оставляй "null"
В ключ resume_text добавь короткий текст о кандидате со всеми кейвордами
=== ПРИМЕР ВЫВОДА ===
{"index": {"_id": "1"}}
{"name": "Дмитрий Волков", "age": 29, "experience": {"years": 4, "position": "Data Analyst", "industry": "banking"}, "skills": {"python": ["pandas", "matplotlib", "seaborn"], "databases": ["PostgreSQL", "Redshift"]}, "achievements": ["Автоматизировал отчётность — сократил время подготовки на 70%"], "english_level": "B1", "applied_at": "2026-04-28"}
"""

    data = {
    "model": "Qwen/Qwen3-8B-AWQ",
    "messages": [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": candidates}
    ],
    "max_tokens": 8192,
    "temperature": 0.7,
    "chat_template_kwargs": {"enable_thinking": False}
    }

    response = requests.post(url, json=data)
    return response.json()["choices"][0]["message"]["content"]

cand = """ 
=== РЕЗЮМЕ 1 — Tabular / HR-формат ===

ФИО: Игорь Белов
Дата рождения: 15.03.1990 (35 лет)
Город: Санкт-Петербург | Готов к переезду: нет | Удалёнка: да
Контакты: igor.belov@gmail.com | +7 921 456-78-90 | t.me/igorbelov

ОПЫТ РАБОТЫ:
2021–н.в. │ Senior Data Scientist │ Сбер │ Москва
          │ - Разработка моделей скоринга для малого бизнеса
          │ - A/B тестирование, рост конверсии на 14%
          │ - Стек: Python, LightGBM, Spark, Hive, Airflow

2018–2021 │ Data Analyst │ ВТБ │ Санкт-Петербург
          │ - Построение отчётности в Tableau
          │ - SQL-оптимизация запросов, ускорение на 3x

ОБРАЗОВАНИЕ: МГУ, Факультет ВМК, бакалавр, 2012
ЯЗЫКИ: Русский (родной), Английский (B2), Немецкий (A2)
ЗАРПЛАТА: от 420 000 руб/мес
НАВЫКИ: Python, Spark, LightGBM, XGBoost, Airflow, PostgreSQL, Hive, Tableau, Docker
KAGGLE: топ-5% в 2 соревнованиях по табличным данным


=== РЕЗЮМЕ 2 — Свободный текст / "письмо о себе" ===

Привет! Меня зовут Екатерина, мне 27. Я занимаюсь компьютерным зрением уже почти 3 года.
Сейчас работаю в небольшой продуктовой компании Visionify (Москва) — делаем промышленный
контроль качества на конвейерах с помощью CV. Моя основная задача — детекция дефектов
на изображениях с производственных камер.

Из стека: PyTorch само собой, OpenCV, YOLO (v5, v8), немного ONNX для экспорта моделей
в прод. Умею в Docker, пишу на Python уровня middle. С SQL работаю редко, но PostgreSQL
знаю достаточно. Английский свободный, читаю документацию и статьи без проблем — C1.

Из достижений — наша команда снизила процент брака на производстве у одного из клиентов
с 2.1% до 0.4%. Я отвечала за пайплайн обучения и деплой модели.

Ищу компанию где есть интересные CV-задачи, желательно не в enterprise. Зарплатные
ожидания — 300к+. Фамилия: Орлова. Почта: kate.orlova.cv@yandex.ru


=== РЕЗЮМЕ 3 — LinkedIn-стиль / английский язык ===

Nikolay Tsvetkov
Age: 33 | Moscow, Russia | Remote only
📧 n.tsvetkov@proton.me | 🔗 linkedin.com/in/ntsvetkov | 💻 github.com/ntsvetkov

SUMMARY
NLP Engineer with 5+ years of experience building production-grade text processing
systems. Specialized in search relevance, information extraction, and LLM fine-tuning.

EXPERIENCE
NLP Engineer — Ozon (2022 – present)
• Built a product search ranking model; improved nDCG@10 by 0.08
• Fine-tuned ruBERT for category classification (94% accuracy, 15M SKUs)
• Deployed models via FastAPI + Docker + K8s; p99 latency < 80ms

NLP Researcher — ABBYY (2019 – 2022)
• Named entity recognition for legal documents
• Published 1 paper at EMNLP workshop 2021

SKILLS
Languages: Python, SQL (ClickHouse, PostgreSQL)
Frameworks: PyTorch, HuggingFace Transformers, spaCy, FastAPI
Infra: Docker, Kubernetes, Kafka, Airflow

EDUCATION: MIPT — M.Sc. Applied Mathematics & Physics, 2015
LANGUAGES: Russian (native), English (C1)
SALARY: 500 000 RUB / negotiable
"""
print(request_llm(cand))