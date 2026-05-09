def extract_header_fields(lines: list[str]) -> dict:
    result = {
        "title": None,
        "company": None,
        "format": None,
        "experience_level": None,
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

        elif "ориентир по рынку" in low or low.startswith("зарплата:") or low.startswith("доход:"):
            result["salary_hint"] = line.split(":", 1)[-1].strip()

    return result