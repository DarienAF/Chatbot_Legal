from fastapi import FastAPI, Query
from utils.search_engine import BuscadorLegal

# Instancia de la aplicacion web
app = FastAPI(title="LegalBot Semántico")

# Instancia del buscador al iniciar
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
    Endpoint de prueba: recibe una consulta 'q', busca en el corpus legal
    y genera una respuesta en lenguaje natural.
    """
    resultados = buscador.buscar(q, k)
    umbral = 1.0

    #Verifica si todos los resultados significativos
    if not all(resultado["distancia"] <= umbral for resultado in resultados[:3]):
        return {
            "consulta": q,
            "top_k": k,
            "resultados": resultados,
            "mensaje": "No se encontró información relevante en el corpus.",
            "disclaimer": "Este asistente no sustituye asesoramiento legal profesional."
        }

    return {
        "consulta": q,
        "top_k": k,
        "resultados": resultados,
        "disclaimer": "Este asistente no sustituye asesoramiento legal profesional."
    }
