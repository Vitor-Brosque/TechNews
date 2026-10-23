from pathlib import Path
from dotenv import load_dotenv
from repositories.hacker_news_carregarsql import salvar_noticia_sql
from repositories.hacker_news_coleta import coletar_dados
from repositories.hacker_news_extracao_validao_url import validar_noticias
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("technews.log", mode="a", encoding="utf-8")],
)
logger = logging.getLogger("technews")

caminho_env = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(caminho_env)


def ingerir():
    noticias = coletar_dados()
    noticias_validas = validar_noticias(noticias)

    salvar_noticia_sql(noticias_validas)


ingerir()
