from .vacancy_constants import *
from .vacancy_common import *

def find_section_positions(text: str) -> list[tuple[int, str]]:
    positions = []

    for section_name, pattern in SECTION_PATTERNS.items():
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            positions.append((match.start(), section_name))

    positions.sort(key=lambda x: x[0])
    return positions


def extract_sections(text: str) -> dict:
    sections = {key: [] for key in SECTION_PATTERNS.keys()}
    positions = find_section_positions(text)

    if not positions:
        return sections

    for i, (start_pos, section_name) in enumerate(positions):
        end_pos = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        chunk = text[start_pos:end_pos]

        chunk = re.sub(
            SECTION_PATTERNS[section_name],
            "",
            chunk,
            count=1,
            flags=re.IGNORECASE
        ).strip(" :\n")

        items = split_lines(chunk)
        items = normalize_section_items(items)
        sections[section_name].extend(items)

    for key in sections:
        sections[key] = normalize_section_items(sections[key])

    return sections


import re
from .vacancy_constants import FALLBACK_TECH_TAGS, TERM_MAP


def extract_fallback_tags(text: str) -> list[str]:
    if not text:
        return []

    low = text.lower()
    found = []

    for tag in FALLBACK_TECH_TAGS:
        pattern = rf"(?<!\w){re.escape(tag.lower())}(?!\w)"
        if re.search(pattern, low, flags=re.IGNORECASE):
            normalized = TERM_MAP.get(tag.lower(), tag.lower())
            if normalized not in found:
                found.append(normalized)

    return found



def build_vacancy_text(parsed: dict, raw_text: str) -> str:
    parts = []

    if parsed.get("title"):
        parts.append(f"Должность: {parsed['title']}")

    if parsed.get("company"):
        parts.append(f"Компания: {parsed['company']}")

    if parsed.get("format"):
        parts.append(f"Формат: {parsed['format']}")

    if parsed.get("experience_level"):
        parts.append(f"Уровень/опыт: {parsed['experience_level']}")

    if parsed.get("required_years") is not None:
        parts.append(f"Требуемый опыт: {parsed['required_years']} лет")

    if parsed.get("salary_hint"):
        parts.append(f"Зарплата: {parsed['salary_hint']}")

    if parsed.get("must_have"):
        parts.append("Обязательные требования: " + " ".join(parsed["must_have"]))

    if parsed.get("requirements"):
        parts.append("Требования: " + " ".join(parsed["requirements"]))

    if parsed.get("responsibilities"):
        parts.append("Обязанности: " + " ".join(parsed["responsibilities"]))

    if parsed.get("conditions"):
        parts.append("Условия: " + " ".join(parsed["conditions"]))

    if parsed.get("tags"):
        parts.append("Стек: " + ", ".join(parsed["tags"]))

    vacancy_text = "\n".join(parts).strip()

    filled_fields = sum([
        bool(parsed.get("title")),
        bool(parsed.get("company")),
        bool(parsed.get("format")),
        bool(parsed.get("experience_level")),
        parsed.get("required_years") is not None,
        bool(parsed.get("must_have")),
        bool(parsed.get("requirements")),
        bool(parsed.get("responsibilities")),
        bool(parsed.get("tags")),
    ])

    if len(vacancy_text) < 100 or filled_fields < 3:
        return raw_text

    return vacancy_text