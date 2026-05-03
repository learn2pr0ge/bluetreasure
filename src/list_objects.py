from opensearchpy import OpenSearch
from .make_embed import similar

# Вывести список всех кандидатов из Opensearch
client = OpenSearch(
        hosts=[{"host": "opensearch", "port": 9200}], # для запуска через docker-compose поменять на 172.23.0.4
        http_auth=("admin", "bestteam1984A."),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False
    )
# Добавляем к каждому кандидату косинусное растояние ембедингов с вакансией
def add_cosinus():
    response = client.search(
        index="vacancy",
        body={"query": {"match_all": {}}, "size": 100}
    )
    vacancy_text = response['hits']['hits'][0]['_source']['vacancy_text']

    response_candidates = client.search(
        index="candidates",
        body={"query": {"match_all": {}}, "size": 100}
    )
    for candidate in response_candidates['hits']['hits']:
        doc_id = candidate['_id']
        resume_text = candidate['_source']['resume_text']
        cos_score = similar(vacancy_text, resume_text)
        client.update(
            index="candidates",
            id=doc_id,
            body={
                "doc": {
                    "cosinus_score": cos_score
                }
            }
        )
    return 1


def show_objects():


    response = client.search(
        index="vacancy",
        body={"query": {"match_all": {}}, "size": 100}
    )
    vacancy_text = response['hits']['hits'][0]['_source']['vacancy_text']

    response_candidates = client.search(
        index="candidates",
        body={"query": {"match_all": {}}, "size": 100}
    )
    # сохраняем кандитатов в словарь
    result_candidates = {}

    for candidate in response_candidates['hits']['hits']:
        doc_id = candidate['_id']
        resume_text = candidate['_source']['resume_text']
        cos_info = candidate['_source']['cosinus_score']
        result_candidates[doc_id] = resume_text + '\n\n' + 'Косинусное растояние с вакансией по эмбедингам модели(intfloat/multilingual-e5-base):' + str(cos_info)
    # переводим словарь в текст для отображения
    candidate_text = ''
    for id, resume in result_candidates.items():
        candidate_text = candidate_text + 'Index: ' + id + '\n\n' + resume + '\n\n'
    candidate_text = candidate_text.replace('\n', '<br>')
    return vacancy_text, candidate_text






