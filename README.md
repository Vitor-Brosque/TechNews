# TechNews

Pipeline em Python que reúne as notícias de tecnologia dos temas que eu acompanho, para eu ler o que importa toda manhã.

**[Estudo de caso no portfólio](https://vitor-brosque.github.io/projetos/technews/)**

## Por que

Acompanhar tecnologia virou um problema de volume. São vários portais e muita notícia por dia, e eu ficava perdido, sem saber o que valia a leitura.

O TechNews é a minha resposta, e foi desenhado assim: busca as notícias dos temas que eu acompanho, guarda no banco, passa por uma IA que filtra, classifica e resume, e me mostra o resultado numa tela, para eu ler toda manhã. O que eu gostar, eu salvo. O que eu não salvar tem prazo para ser apagado quando chegam as novas.

Ele também é o meu laboratório de engenharia de dados: cada etapa é construída para eu entender o porquê de cada decisão.

## Das fontes à leitura da manhã

| Etapa | O que acontece |
| --- | --- |
| **Fontes** | As notícias vêm de portais e APIs de tecnologia, sempre dos temas que eu acompanho. Cada fonte tem o seu coletor, e um fallback assume quando uma fonte falha. |
| **Coleta** | Cada coletor busca as notícias do dia anterior, no fuso de São Paulo. O do Hacker News consulta a API de busca sobre 10 temas em 4 áreas: linguagens, IA, dados e DevOps. O que vem sem título ou sem URL, ou repetido entre temas, é descartado e registrado no log. |
| **Extração** | Baixa a página original e extrai o texto com o trafilatura. Falha no download ou na extração é registrada, e a notícia é pulada. |
| **PostgreSQL** | Grava com `INSERT ... ON CONFLICT (fonte, id_externo) DO NOTHING RETURNING id`. Se não voltou id, era duplicada. No fim, um log diz quantas notícias foram inseridas, quantas eram duplicadas e quantas foram rejeitadas. |
| **IA** | As notícias guardadas no banco passam por uma IA, que filtra, classifica e resume cada uma. |
| **Leitura da manhã** | O resultado aparece numa tela, para eu ler as novidades toda manhã. O que eu gostar, eu salvo. O que não salvar tem prazo para ser apagado quando chegam as novas. |

## Decisões técnicas

| Decisão | Por quê | O que ficou de lado |
| --- | --- | --- |
| **Idempotência no banco:** chave única em `(fonte, id_externo)` e `INSERT ... ON CONFLICT DO NOTHING RETURNING id` | Rodar o pipeline de novo, de propósito ou por engano, não duplica notícias. E o `RETURNING` diz, sem uma consulta extra, se a linha era nova ou repetida | Checar se a notícia existe antes de inserir, que custa uma consulta a mais e ainda deixa uma janela para duplicar |
| **Uma notícia ruim não derruba o lote:** commit por notícia | Num pipeline de ingestão, dado estranho é normal. Um erro desfaz só aquela linha, que entra na conta das rejeitadas, e o resto do lote segue | Uma transação única para o lote, mais rápida, mas que perde tudo por causa de uma linha |
| **Logs com nome de evento:** eventos com nome fixo, sempre com o id da notícia | Dá para achar qualquer falha com uma busca no arquivo de log e contar o que aconteceu em cada execução | Mensagens livres, mais fáceis de escrever e difíceis de filtrar |
| **Janela de tempo fechada:** cada execução busca o dia anterior inteiro, no fuso de São Paulo | A mesma execução, repetida no mesmo dia, pega o mesmo conjunto. O resultado fica previsível e fácil de conferir | As "últimas 24 horas" a partir de agora, que mudam a cada execução |

## Como rodar

Com o PostgreSQL configurado:

```bash
python scr/main.py
```

O log vai para `technews.log`, no formato `data e hora | nível | mensagem`.

## Situação atual

O projeto está no começo. Hoje existe a primeira parte do fluxo: a coleta no Hacker News, a validação, a extração do texto e a gravação no PostgreSQL. Numa execução de teste em 23/11/2026, ele coletou 81 notícias e extraiu o texto de 70 delas (86%).

Agora estou decidindo as próximas fontes e criando os coletores que alimentam o banco, com os fallbacks. A IA e a tela de leitura já estão desenhadas e vêm em seguida.

## Stack

Python · PostgreSQL · psycopg 3 · httpx · trafilatura · API do Hacker News

<details>
<summary><b>In English</b></summary>
<br>
A Python pipeline that gathers tech news on the topics I follow, so I can read what matters every morning. It was designed to collect news from several sources, store it in PostgreSQL, run it through an AI that filters, classifies and summarizes, and show the result on a screen to read every morning. Today the first part exists: collecting from the Hacker News API, validation, text extraction and idempotent storage in PostgreSQL. Case study: <a href="https://vitor-brosque.github.io/en/projects/technews/">vitor-brosque.github.io/en/projects/technews</a>.
</details>

---

Vitor Brosque · [LinkedIn](https://www.linkedin.com/in/vitorbrosque) · [Portfólio](https://vitor-brosque.github.io)
