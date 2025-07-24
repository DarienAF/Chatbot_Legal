from fastapi import FastAPI, Query
from utils.search_engine import BuscadorLegal

app = FastAPI(title="LegalBot Semántico")

# Instancia el buscador al iniciar
buscador = BuscadorLegal(corpus_path='legal_corpus')

@app.get("/")
def root():
    return {"mensaje": "LegalBot Semántico activo"}

@app.get("/test_busqueda")
def test_busqueda(
    q: str = Query(..., description="Consulta legal para buscar en el corpus"),
    k: int = Query(3, description="Número de fragmentos que se retornarán")
):
    """
    Endpoint de prueba: recibe una consulta 'q' y retorna los k fragmentos
    más similares según el índice semántico.
    """
    resultados = buscador.buscar(q, k)
    return {
        "consulta": q,
        "top_k": k,
        "resultados": resultados
    }
