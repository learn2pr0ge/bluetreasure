from .vacancy_common import *
from .vacancy_header import *
from .vacancy_scetions import *

def parse_vacancy_text(raw_text: str) -> dict:
    raw_text = clean_text(raw_text)
    lines = split_lines(raw_text)

    header = extract_header_fields(lines)
    sections = extract_sections(raw_text)

    parsed = {
        **header,
        **sections,
        "raw_text": raw_text,
    }

    parsed["vacancy_text"] = build_vacancy_text(parsed, raw_text)
    return parsed


def parse_vacancy_pdf(pdf_path: str) -> dict:
    raw_text = extract_text_from_pdf(pdf_path)
    return parse_vacancy_text(raw_text)