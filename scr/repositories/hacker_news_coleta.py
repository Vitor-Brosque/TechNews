import httpx
import logging

logger = logging.getLogger("technews")


def coletar_dados():
    url = "https://hn.algolia.com/api/v1/search_by_date?tags=story"
    dados = httpx.get(url)
    dados.raise_for_status()
    dados_dict = dados.json()
    lista_de_noticias = []
    for noticias in dados_dict["hits"]:
        if noticias.get("url") is not None:
            dicit_temp = {
                "criacao": noticias.get("created_at"),
                "ID": noticias.get("objectID"),
                "Titulo": noticias.get("title"),
                "url": noticias.get("url"),
                "Fonte": "Hacker News",
                "Conteudo": None,
            }
            lista_de_noticias.append(dicit_temp)
        else:
            logging.warning("SEM URL | ID = %s", noticias.get("objectID"))
            continue
    return lista_de_noticias
