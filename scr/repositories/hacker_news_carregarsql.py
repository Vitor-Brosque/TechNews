import os
import psycopg
import logging
from datetime import datetime

logger = logging.getLogger("technews")


def conectar():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def testar_conexao():
    try:
        with conectar() as conexao:

            with conexao.cursor() as cursor:
                cursor.execute("SELECT current_database();")
                resultado = cursor.fetchone()

                logger.info("POSTGRES_CONECTADO | DB = %s", resultado[0])
            return True

    except psycopg.OperationalError:
        logger.exception("FALHA_CONEXAO_POSTGRES")
        raise


def salvar_noticia_sql(noticias):
    noticias_incluidas_sucesso = []
    noticias_duplicadas = []
    noticias_falha_inclusao = []

    try:
        with conectar() as conexao:
            with conexao.cursor() as cursor:
                for noticia in noticias:
                    try:
                        cursor.execute(
                            """
                            INSERT INTO noticias (
                            id_externo,
                            titulo,
                            url,
                            fonte,conteudo,
                            criado_na_fonte_em
                            )
                            VALUES(%s,%s,%s,%s,%s,%s)
                            ON CONFLICT (fonte,id_externo) DO NOTHING
                            RETURNING id;
                            """,
                            (
                                noticia.get("ID"),
                                noticia.get("Titulo"),
                                noticia.get("url"),
                                noticia.get("Fonte"),
                                noticia.get("Conteudo"),
                                noticia.get("criacao"),
                            ),
                        )
                        resultado = cursor.fetchone()
                        conexao.commit()
                    except (psycopg.DataError, psycopg.IntegrityError):
                        conexao.rollback()

                        noticias_falha_inclusao.append(noticia.get("ID"))
                        logger.exception(
                            "NOTICIA_REJEITADA | ID = %s", noticia.get("ID")
                        )
                        continue

                    if resultado is None:
                        noticias_duplicadas.append(noticia.get("ID"))

                    else:
                        noticias_incluidas_sucesso.append(noticia.get("ID"))

    except psycopg.Error:
        logger.exception("INGESTAO_INTERROMPIDA | ERRO_SQL_OU_CONEXAO")
        raise
    logger.info(
        "RESUMO_INGESTAO | INSERIDAS=%s | DUPLICADAS=%s | REJEITADAS=%s",
        len(noticias_incluidas_sucesso),
        len(noticias_duplicadas),
        len(noticias_falha_inclusao),
    )
