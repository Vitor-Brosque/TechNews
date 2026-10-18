import trafilatura
import logging

logger = logging.getLogger("technews")


def validar_noticias(dicionarios):
    noticias_validas = []

    for dicionario in dicionarios:
        url = dicionario.get("url")
        id_noticia = dicionario.get("ID")

        html = trafilatura.fetch_url(url)

        if html is None:
            logging.warning("FALHA_DOWNLOAD | ID=%s | URL=%s", id_noticia, url)
            continue

        texto = trafilatura.extract(html)

        if texto is None or not texto.strip():
            logging.warning("FALHA_EXTRACAO | ID = %s | URL = %s ", id_noticia, url)
            continue

        dicionario["Conteudo"] = texto
        noticias_validas.append(dicionario)

        logging.info("EXTRACAO_OK | ID = %s", id_noticia)

    return noticias_validas
