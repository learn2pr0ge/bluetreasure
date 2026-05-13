import re

TERM_MAP = {
    "golang": "go",

    "питон": "python",
    "джава": "java",
    "яваскрипт": "javascript",
    "js": "javascript",
    "тайпскрипт": "typescript",
    "ts": "typescript",

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "scikit-learn": "scikit-learn",

    "микросервис": "microservices",
    "микросервисный": "microservices",
    "microservice": "microservices",

    "лидерство": "lead",
    "лидер": "lead",
    "тимлид": "lead",
    "тимлида": "lead",
    "тимлидер": "lead",
    "руководитель": "lead",

    "менторинг": "mentoring",
    "наставничество": "mentoring",

    "постгрес": "postgresql",
    "postgres": "postgresql",
    "pg": "postgresql",

    "монго": "mongodb",
    "mongo": "mongodb",

    "эластик": "elasticsearch",
    "elastic": "elasticsearch",

    "кубернетес": "kubernetes",
    "кубернетёс": "kubernetes",
    "кубер": "kubernetes",
    "k8s": "kubernetes",

    "докер": "docker",

    "оптимизация": "optimization",
    "проектирование": "design",
    "архитектура": "architecture",
    "архитектурный": "architecture",
    "тестирование": "testing",
    "мониторинг": "monitoring",
    "развёртывание": "deploy",
    "деплой": "deploy",
    "deployment": "deploy",

    "разработка": "development",
    "бэкенд": "backend",
    "бекенд": "backend",
    "фронтенд": "frontend",
    "фулстек": "fullstack",
    "full-stack": "fullstack",

    "скрам": "scrum",
    "аджайл": "agile",
    "канбан": "kanban",

    "распределённый": "distributed",
    "высоконагруженный": "highload",
    "масштабируемость": "scalability",
    "производительность": "performance",
    "отказоустойчивость": "fault_tolerance",

    "а/б-тестирование":'a/b testing',
    "a/b-тестирование":'a/b testing',
    "а/b-тестирование":'a/b testing',
    "а/в-тестирование":'a/b testing',
    "a/в-тестирование":'a/b testing',
    
    "ab testing": "a/b testing",
    "аб тестирование": "a/b testing",
    "машинное обучение": "machine learning",
    "машинного обучения": "machine learning",
    "natural language processing": "nlp",

    "llm":'llm'
}

CANONICAL_TECH_TAGS = [
    "python",
    "sql",
    "postgresql",
    "mongodb",
    "redis",
    "clickhouse",
    "airflow",
    "spark",
    "hadoop",
    "etl",
    "dwh",
    "docker",
    "kubernetes",
    "helm",
    "grafana",
    "prometheus",
    "victoriametrics",
    "vault",
    "rabbitmq",
    "kafka",
    "nats",
    "linux",
    "bash",
    "java",
    "go",
    "javascript",
    "typescript",
    ".net",
    "c++",
    "ci/cd",
    "gitlab ci/cd",
    "backend",
    "frontend",
    "fullstack",

    # ML / DS / LLM
    "pandas",
    "numpy",
    "scipy",
    "matplotlib",
    "seaborn",
    "plotly",
    "scikit-learn",
    "xgboost",
    "lightgbm",
    "catboost",
    "optuna",
    "mlflow",
    "pytorch",
    "tensorflow",
    "keras",
    "transformers",
    "opencv",
    "nltk",
    "spacy",
    "fastapi",
    "flask",
    "llm",
    "a/b testing",
    "machine learning",
    "nlp",
    "mlops",
]

FALLBACK_TECH_TAGS = sorted(
    set(TERM_MAP.keys()) | set(TERM_MAP.values()) | set(CANONICAL_TECH_TAGS),
    key=len,
    reverse=True,
)

_SPLIT_RE = re.compile(r"[,;|]+")
_WORD_RE = re.compile(r"[a-zа-я0-9\.\+#\-]+", flags=re.IGNORECASE)


def normalize_term(value: str) -> str:
    value = value.lower().strip()
    return TERM_MAP.get(value, value)

SEARCH_TERMS = sorted(
    set(TERM_MAP.keys()) | set(TERM_MAP.values()) | set(CANONICAL_TECH_TAGS),
    key=len,
    reverse=True,
)


def extract_tags_from_text(text: str) -> list[str]:
    if not text:
        return []

    low = text.lower()
    found = []

    for term in SEARCH_TERMS:
        if term in low:
            found.append(TERM_MAP.get(term, term))

    return sorted(set(found))

def normalize_tags(tags: list[str]) -> set[str]:
    result = set()

    for tag in tags:
        if not isinstance(tag, str):
            continue

        tag = tag.lower().strip()
        if not tag:
            continue

        parts = re.split(r"[,;|]+", tag)

        for part in parts:
            part = part.strip()
            if not part:
                continue

            token = TERM_MAP.get(part, part)
            if len(token) > 1:
                result.add(token)

    return result