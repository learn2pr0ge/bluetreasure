import re
from .vacancy_constants import *

def extract_required_years_from_experience(text: str | None) -> float | None:
    if not text:
        return None

    low = text.lower().strip()

    # "от 3 лет"
    m = re.search(r"от\s+(\d+(?:[.,]\d+)?)\s*(?:лет|года|год)", low)
    if m:
        return float(m.group(1).replace(",", "."))

    # "3-5 лет" / "3 – 5 лет"
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*[-–—]\s*(\d+(?:[.,]\d+)?)\s*(?:лет|года|год)", low)
    if m:
        return float(m.group(1).replace(",", "."))

    # "3+ лет"
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*\+\s*(?:лет|года|год)?", low)
    if m:
        return float(m.group(1).replace(",", "."))

    # просто "3 года"
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:лет|года|год)", low)
    if m:
        return float(m.group(1).replace(",", "."))

    # уровни
    for level, years in LEVEL_TO_YEARS.items():
        if level in low:
            return years

    return None




def extract_header_fields(lines: list[str]) -> dict:
    result = {
        "title": None,
        "company": None,
        "format": None,
        "experience_level": None,
        "required_years": None,
        "salary_hint": None,
    }

    if lines:
        result["title"] = lines[0]

    for line in lines[:15]:
        low = line.lower()

        if low.startswith("компания:"):
            result["company"] = line.split(":", 1)[1].strip()

        elif low.startswith("формат:"):
            result["format"] = line.split(":", 1)[1].strip()

        elif low.startswith("опыт:"):
            result["experience_level"] = line.split(":", 1)[1].strip()
            result["required_years"] = extract_required_years_from_experience(result["experience_level"])

        elif "ориентир по рынку" in low or low.startswith("зарплата:") or low.startswith("доход:"):
            result["salary_hint"] = line.split(":", 1)[-1].strip()

    return result