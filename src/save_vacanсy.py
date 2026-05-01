from opensearchpy import OpenSearch


# Проверка наличия индекса

client = OpenSearch(
    hosts=[{"host": "opensearch", "port": 9200}], # для запуска через docker-compose поменять на 172.23.0.4
    http_auth=("admin", "bestteam1984A."),
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False
)

def create_index(vacancy):
    if client.indices.exists(index='vacancy'):
        # если индекс есть до удаляем все данные из него (нужно для повторных запусков)
        client.indices.delete(index='vacancy')
        # создаем индекс заново и кладем в него текст вакансии
        mapping = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "vacancy_text": {"type": "text"}
                }
            }
        }
        response_os = client.indices.create(index='vacancy', body=mapping)
        document = {
            "vacancy_text": vacancy,
        }
        response_os_after_creation = client.index(
            index="vacancy",
            body=document
        )

        return response_os_after_creation
    else:
        mapping = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "vacancy_text": {"type": "text"}
                }
            }
        }
        response_os = client.indices.create(index='vacancy', body=mapping)
        document = {
            "vacancy_text": vacancy,
        }
        response_os_after_creation = client.index(
            index="vacancy",
            body=document
        )

        return response_os_after_creation







