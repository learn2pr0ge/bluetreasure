from opensearchpy import OpenSearch

# Вывести список всех кандидатов из Opensearch
client = OpenSearch(
        hosts=[{"host": "opensearch", "port": 9200}], # для запуска через docker-compose поменять на 172.23.0.4
        http_auth=("admin", "bestteam1984A."),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False
    )


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
        result_candidates[doc_id] = resume_text
    # переводим словарь в текст для отображения
    candidate_text = ''
    for id, resume in result_candidates.items():
        candidate_text = candidate_text + 'Index: ' + id + '\n\n' + resume + '\n\n'
    candidate_text = candidate_text.replace('\n', '<br>')
    return vacancy_text, candidate_text






