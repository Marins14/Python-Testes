import logging
from pathlib import Path
from .db import get_connection

# dir = Path.home() / "Documentos/Python-Testes/locadora/logs/locadora.log"

# logging.basicConfig(
#    filename=dir,
#    level=logging.INFO,
#    format="%(asctime)s :: [%(levelname)s] :: %(message)s",
#    datefmt="%Y-%m-%d %H:%M:%S",
# )

def criar_tabela():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            quantidade INT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
#     logging.info("Tabela criada com sucesso!")
#     print("Tabela criada com sucesso!")


def listar_filmes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM filmes;")
    result = cur.fetchall()

    cur.close()
    conn.close()
    return result


def buscar_filmes(titulo):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM filmes WHERE unaccent(titulo) ILIKE unaccent(%s);",
        (f"%{titulo}%",),
    )
    result = cur.fetchall()

    cur.close()
    conn.close()
    return result


def remover_filmes(titulo, quantos):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE filmes SET quantidade = GREATEST(quantidade - %s, 0) WHERE unaccent(titulo) = unaccent(%s) RETURNING *;",
        (quantos, titulo),
    )
    result = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    return result


def inclui_filmes(titulo, quantidade):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO filmes(titulo,quantidade) VALUES(%s,%s) RETURNING *;",
        (
            titulo,
            quantidade,
        ),
    )

    result = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()
    # logging.info(
    #    "O Seguinte dado foi inserido na tabela: {}, {}".format(titulo, quantidade)
    # )
    return result


def excluir_filmes(titulo):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM filmes WHERE unaccent(titulo) = unaccent(%s) RETURNING *;",
        (titulo,),
    )
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    # logging.info("O Seguinte filme foi removido da tabela: {}".format(titulo))
    return result
