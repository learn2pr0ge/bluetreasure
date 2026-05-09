from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-base", device="cpu")


def build_resume_text(doc: dict) -> str:
    parts = []

    if doc.get("name"):
        parts.append(doc["name"])

    contacts = doc.get("contacts", {})
    if contacts.get("location"):
        parts.append(f"Локация: {contacts['location']}")

    exp = doc.get("experience", {})
    if exp.get("years") is not None:
        parts.append(f"Опыт: {exp['years']} лет")

    for pos in exp.get("positions", []):
        role = pos.get("role")
        company = pos.get("company")

        responsibilities = pos.get("responsibilities")
        if isinstance(responsibilities, list):
            responsibilities = " ".join(responsibilities)

        block = " ".join(x for x in [role, company, responsibilities] if x)
        if block:
            parts.append(block)

    skills = doc.get("skills", {})
    if skills.get("tools"):
        parts.append("Навыки: " + ", ".join(skills["tools"]))

    if skills.get("languages"):
        parts.append("Языки: " + ", ".join(skills["languages"]))

    edu = doc.get("education", {})
    if edu.get("institution"):
        parts.append(f"Образование: {edu['institution']}")

    if doc.get("achievements"):
        if isinstance(doc["achievements"], list):
            parts.append("Достижения: " + " ".join(doc["achievements"]))
        else:
            parts.append("Достижения: " + str(doc["achievements"]))

    return "\n".join(parts)


def embed_resume(text: str) -> list[float]:
    return model.encode(f"passage:{text}", normalize_embeddings=True).tolist()


def embed_vacancy(text: str) -> list[float]:
    return model.encode(f"query:{text}", normalize_embeddings=True).tolist()