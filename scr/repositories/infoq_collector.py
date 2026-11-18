import feedparser
import httpx


def coletar_dados():
    url = "https://feed.infoq.com/Programming"
    resposta = httpx.get(url)
    resposta.raise_for_status()
    dados = feedparser.parse(resposta.content)

    print(dados.keys())
    print(len(dados.entries))


coletar_dados()
