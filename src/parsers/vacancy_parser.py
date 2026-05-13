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

    raw_tags = parsed.get("tags") or []

    if isinstance(raw_tags, str):
        raw_tags = [raw_tags]

    tag_source = " ".join(x for x in raw_tags if isinstance(x, str) and x.strip())

    if tag_source:
        parsed["tags"] = extract_fallback_tags(tag_source)
    else:
        fallback_source = " ".join(
            x for x in [parsed.get("title"), raw_text] if x
        )
        parsed["tags"] = extract_fallback_tags(fallback_source)

    parsed["vacancy_text"] = build_vacancy_text(parsed, raw_text)
    return parsed


def parse_vacancy_pdf(pdf_source) -> dict:
    raw_text = extract_text_from_pdf(pdf_source)
    return parse_vacancy_text(raw_text)