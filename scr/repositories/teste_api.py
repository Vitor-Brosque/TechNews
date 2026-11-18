import json

import httpx

url = """api.gdeltproject.org/api/v2/doc/doc?query=("climate change" OR "global warming")&mode=artlist&maxrecords=200&timespan=1h&sort=datedesc&format=JSON"""
requisicao = httpx.get(url)
conteudo_json = requisicao.json()

with open("dados.json", "w", encoding="utf8") as file:
    json.dump(conteudo_json, file, indent=5)
