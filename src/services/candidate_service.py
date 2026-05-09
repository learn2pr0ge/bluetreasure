from ..parsers.candidate_parser import *
from ..embeddings.make_embed import * 


def parse_data_full(data_full: dict) -> dict:
    parsed = {}

    for filename, data in data_full.items():
        candidate = parse_resume(data)
        candidate["source_file"] = filename
        candidate['resume_text'] = build_resume_text(candidate)
        candidate['resume_vector'] = embed_resume(candidate['resume_text'])
        parsed[filename] = candidate

    return parsed


def prepare_candidate_doc(parsed: dict, source_file: str) -> dict:
    doc = parsed.copy()
    doc["source_file"] = source_file
    doc["resume_text"] = build_resume_text(doc)
    doc["resume_vector"] = embed_resume(doc["resume_text"])
    return doc


def ingest_candidate_pdfs(files) -> dict:
    docs = {}
    loaded = 0
    errors = 0

    for file in files:
        try:
            data = read_resume_pdf_raw(file)
            parsed = parse_resume(data)
            doc = prepare_candidate_doc(parsed, file.filename)
            docs[file.filename] = doc
            loaded += 1
        except Exception:
            errors += 1

    if docs:
        bulk_index_parsed_candidates(client, docs, index_name="candidates")

    return {
        "loaded": loaded,
        "errors": errors,
        "duplicates": 0
    }