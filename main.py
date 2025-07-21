from fastapi import FastAPI, Query
from utils.search_engine import BuscadorLegal

app = FastAPI()
buscador = BuscadorLegal()

@app.get("/")
def root():
    return {"mensaje": "Servidor legal activo"}

@app.get("/test_busqueda")
def test_busqueda(q: str = Query(..., description="Consulta legal")):
    resultados = buscador.buscar(q)
    return {"consulta": q, "resultados": resultados}
