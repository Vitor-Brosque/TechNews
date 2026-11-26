import json
import logging
from datetime import datetime, time, timedelta, timezone

import httpx

logger = logging.getLogger("technews")


def req_httpx(url, params=None):
    try:
        reponse = httpx.get(url, params=params)
        reponse.raise_for_status()
        return reponse.json()

    except httpx.TimeoutException as e:
        logger.error("Timeout na requisição HTTP: %s", e)
        return None

    except json.JSONDecodeError as e:
        logger.error("Erro ao decodificar JSON: %s", e)
        return None

    except httpx.RequestError as e:
        logger.error("Erro na requisição HTTP: %s", e)
        return None

    except httpx.HTTPStatusError as e:
        logger.error(
            "HTTP_STATUS_ERROR | STATUS=%s | URL=%s",
            e.response.status_code,
            e.request.url,
        )
        return None


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
            f"created_at_i>={int(inicio_formatado)},created_at_i<{int(fim_formatado)}"
        ),
        "hitsPerPage": 50,
        "page": 0,
    }
    lista_de_noticias = []
    set_de_ids = set()

    for temas in pesquisas:
        for topico in pesquisas[temas]:
            params["page"] = 0
            params["query"] = topico
            dados_dict = req_httpx(url_api, params=params)
            if dados_dict is None:
                logger.error("Falha ao obter dados para o tópico: %s", topico)
                continue
            number_pages = dados_dict["nbPages"]
            while number_pages > 0:
                number_pages -= 1
                for noticia in dados_dict["hits"]:
                    if noticia.get("objectID") in set_de_ids:
                        logger.info(
                            "DUPLICIDADE_DE_ID | ID = %s", noticia.get("objectID")
                        )
                        continue
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
                        set_de_ids.add(noticia.get("objectID"))
                    else:
                        logger.warning(
                            "SEM_URL_OU_TITULO | ID = %s", noticia.get("objectID")
                        )
                        continue
                if number_pages == 0:
                    break

                params["page"] += 1
                dados = req_httpx(url_api, params=params)
                dados_dict = dados
                if dados_dict is None:
                    logger.error(
                        "Falha ao obter dados para o tópico: %s na página %d",
                        topico,
                        params["page"],
                    )
                    break

    return lista_de_noticias


if __name__ == "__main__":
    coletar_dados()
