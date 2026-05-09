from ..parsers.candidate_common import read_resume_pdf_raw
from ..parsers.candidate_parser import parse_resume
from ..embeddings.make_embed import build_resume_text
from ..embeddings.make_embed import embed_resume
from ..storage.opensearch_client import get_opensearch_client
from ..storage.opensearch_candidates import (
    candidate_exists,
    bulk_index_candidates,
    create_candidates_index_if_not_exists,
)


def prepare_candidate_doc(parsed: dict, source_file: str) -> dict:
    doc = parsed.copy()
    doc["source_file"] = source_file
    doc["resume_text"] = build_resume_text(doc)
    doc["resume_vector"] = embed_resume(doc["resume_text"])
    return doc


def parse_data_full(data_full: dict) -> dict:
    parsed_docs = {}

    for filename, data in data_full.items():
        parsed = parse_resume(data)
        doc = prepare_candidate_doc(parsed, filename)
        parsed_docs[filename] = doc

    return parsed_docs


def ingest_candidate_pdfs(files) -> dict:
    docs = {}
    loaded = 0
    errors = 0
    duplicates = 0
    error_details = []

    client = get_opensearch_client()
    create_candidates_index_if_not_exists(client)

    for file in files:
        try:
            data = read_resume_pdf_raw(file)
            parsed = parse_resume(data)
            doc = prepare_candidate_doc(parsed, file.filename)

            if candidate_exists(client, file.filename):
                duplicates += 1
                continue

            docs[file.filename] = doc
            loaded += 1

        except Exception as e:
            errors += 1
            error_details.append({
                "file": file.filename,
                "error": str(e),
            })

    if docs:
        bulk_index_candidates(client, docs)

    return {
        "loaded": loaded,
        "errors": errors,
        "duplicates": duplicates,
        "error_details": error_details,
    }