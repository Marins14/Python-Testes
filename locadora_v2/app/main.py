from fastapi import FastAPI
from fastapi import HTTPException
from . import crud

"""
    A ideia é montar um banco de dados relacional que faça uma 'locadora virtual' via API!
"""


app = FastAPI()

@app.get("/filmes")
def lista_filmes():
    return crud.listar_filmes()

@app.get("/filmes/{titulo}")
def buscar(titulo:str):
    filme = crud.buscar_filmes(titulo)

    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme

@app.put("/filmes/remover/{titulo}/{quantidade}")
def remover(titulo: str, quantidade: int):
    filme = crud.remover_filmes(titulo, quantidade)
    if not filme:
        return {"erro": "Filme não encontrado ou quantidade já é zero"}
    return filme

@app.put("/filmes/incluir/{titulo}/{quantidade}")
def incluir(titulo: str, quantidade: int):

    filme_existente = crud.buscar_filmes(titulo)

    if filme_existente:
        return {"erro": f"O filme '{titulo}' já existe na base"}
    filme = crud.inclui_filmes(titulo, quantidade)

    if not filme:
        return {"erro": "Não foi possível incluir o filme"}
    return filme