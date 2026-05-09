import fitz
import re
from .vacancy_constants import *



def extract_text_from_pdf(pdf_source) -> str:
    if hasattr(pdf_source, "stream"):
        pdf_source.stream.seek(0)
        pdf_bytes = pdf_source.stream.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    else:
        doc = fitz.open(pdf_source)

    with doc:
        text = "\n".join(page.get_text("text") for page in doc)

    return text


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = MULTI_NL_RE.sub("\n\n", text)
    return text.strip()


def clean_line(line: str) -> str:
    line = line.replace("\xa0", " ").strip()
    line = SPACE_RE.sub(" ", line)
    line = line.strip("•●▪◦·*-–— ").strip()
    return line


def split_lines(text: str) -> list[str]:
    result = []

    for raw_line in text.splitlines():
        raw_line = raw_line.strip()

        if not raw_line:
            continue

        if BULLET_ONLY_RE.fullmatch(raw_line):
            continue

        line = clean_line(raw_line)

        if not line:
            continue

        if line.lower() in SECTION_HEADERS:
            continue

        result.append(line)

    return result


def normalize_section_items(items: list[str]) -> list[str]:
    result = []

    for item in items:
        item = clean_line(item)

        if not item:
            continue

        # короткие хвосты и продолжения строки приклеиваем к предыдущей
        if result and (
            len(item) <= 25
            or item[0].islower()
            or item.lower() in {"обязательно", "обязательно.", "желательно", "желательно."}
        ):
            result[-1] = result[-1].rstrip(" .;:") + " " + item
        else:
            result.append(item)

    # дедуп
    seen = set()
    unique_result = []
    for item in result:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            unique_result.append(item)

    return unique_result