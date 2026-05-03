from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer(
    "intfloat/multilingual-e5-base",
    device="cpu"
)

def similar(vacancy, resume):
    vacancy_emb = model.encode(f"query:{vacancy}")
    resume_emb = model.encode(f"passage:{resume}")
    score = cosine_similarity([vacancy_emb], [resume_emb])[0][0]
    return round(float(score), 4)

#
#
# print(similar(vacancy, resume))


