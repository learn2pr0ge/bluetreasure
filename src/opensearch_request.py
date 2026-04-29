from opensearchpy import OpenSearch

# Вывести список всех кандидатов из Opensearch

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "bestteam1984A."),
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False
)

response = client.search(
    index="candidates",
    body={"query": {"match_all": {}}, "size": 100}
)

print(response)
