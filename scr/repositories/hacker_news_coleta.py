import httpx
import logging
import time as tempo
from datetime import datetime, timedelta, timezone, time

logger = logging.getLogger("technews")


def coletar_dados():
    fuso = timezone(timedelta(hours=-3))

    hoje = datetime.now(fuso)

    ontem = hoje - timedelta(days=1)

    inicio = datetime.combine(ontem, time.min, tzinfo=fuso)

    fim = inicio + timedelta(days=1)

    inicio_formatado = inicio.timestamp()
    fim_formatado = fim.timestamp()

    url_api = "https://hn.algolia.com/api/v1/search_by_date"

    pesquisas = {
        "Linguagens": ["Python", "Rust", "TypeScript"],
        "IA": ["OpenAI", "Anthropic", "machine learning"],
        "Dados": ["PostgreSQL", "Apache Spark"],
        "DevOps": ["Docker", "Kubernetes"],
    }

    params = {
        "query": pesquisas["Linguagens"][0],
        "tags": "story",
        "numericFilters": (
            f"created_at_i>={int(inicio_formatado)},"
            f"created_at_i<{int(fim_formatado)}"
        ),
    }
    lista_de_noticias = []

    for pesquisa in pesquisas:
        for topico in pesquisas[pesquisa]:
            params["query"] = topico
            dados = httpx.get(url_api, params=params)
            dados.raise_for_status()
            dados_dict = dados.json()
            for noticia in dados_dict["hits"]:
                url_noticia = noticia.get("url")
                titulo = noticia.get("title")
                if (
                    isinstance(url_noticia, str)
                    and url_noticia.strip()
                    and isinstance(titulo, str)
                    and titulo.strip()
                ):
                    dicit_temp = {
                        "criacao": noticia.get("created_at"),
                        "ID": noticia.get("objectID"),
                        "Titulo": noticia.get("title"),
                        "url": noticia.get("url"),
                        "Fonte": "Hacker News",
                        "Conteudo": None,
                    }
                    lista_de_noticias.append(dicit_temp)
                else:
                    logger.warning(
                        "SEM_URL_OU_TITULO | ID = %s", noticia.get("objectID")
                    )
                    continue
    return lista_de_noticias
