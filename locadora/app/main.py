import logging
from db import get_connection
from pathlib import Path

"""
    A ideia é montar um banco de dados relacional que faça uma 'locadora virtual'
"""

dir = Path.home() / "Documentos/Python-Testes/locadora/logs/locadora.log"

logging.basicConfig(filename=dir, 
                    level=logging.INFO, 
                    format='%(asctime)s :: [%(levelname)s] :: %(message)s' ,
                    datefmt='%Y-%m-%d %H:%M:%S')

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
    logging.info("Tabela criada com sucesso!")
    print("Tabela criada com sucesso!")

def inserir_dado(titulo, quantidade):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO filmes (titulo, quantidade) VALUES (%s, %s);", (titulo, quantidade))
    conn.commit()

    cur.close()
    conn.close()
    logging.info("O Seguinte dado foi inserido na tabela: {}, {}".format(titulo, quantidade))
    print("Dado inserido!")

def listar_dados():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM filmes;")
    linhas = cur.fetchall()

    print("Conteúdo da tabela:")
    for linha in linhas:
        print(linha)

    cur.close()
    conn.close()

def remover_dados(titulo):
    conn = get_connection()
    cur = conn.cursor()


    cur.execute(
        "SELECT id, quantidade FROM filmes WHERE titulo ILIKE %s;",
        (titulo,)
    )
    dados = cur.fetchone()

    if not dados:
        logging.error("Nenhum filme encontrado na base com este título: {}".format(titulo))
        print("Nenhum filme encontrado com esse título.")
        cur.close()
        conn.close()
        return

    filme_id, quantidade = dados

    nova_quantidade = max(quantidade - 1, 0)

    cur.execute(
        "UPDATE filmes SET quantidade = %s WHERE id = %s;",
        (nova_quantidade, filme_id)
    )

    conn.commit()
    cur.close()
    conn.close()
    logging.info("A quantidade foi atualizada para {} do titulo: {}".format(nova_quantidade, titulo))
    print(f"Quantidade atualizada para {nova_quantidade}.")

if __name__ == "__main__":
    criar_tabela()
    #inserir_dado("Missão Impossível 1", 29)
    inserir_dado("Rambo 2", 22)
    listar_dados()
    remover_dados("Rambo")
