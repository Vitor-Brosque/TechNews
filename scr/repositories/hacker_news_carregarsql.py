import logging

from hacker_news_coleta import coletar_dados
from hacker_news_extracao_validao_url import validar_noticias

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("technews.log", mode="a", encoding="utf-8")],
)


def ingerir():
    noticias = coletar_dados()
    noticias_validas = validar_noticias(noticias)


if __name__ == "__main__":
    ingerir()
