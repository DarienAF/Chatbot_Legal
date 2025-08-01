from fastapi import FastAPI, Query
from utils.search_engine import BuscadorLegal
from dotenv import load_dotenv
from utils.generator import generar_respuesta_legal


# AI API LLAMA3 from Together.AI (generator.py)
load_dotenv()

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
    Endpoint de prueba: recibe una consulta 'q', busca en el corpus legal
    y genera una respuesta en lenguaje natural.
    """
    resultados = buscador.buscar(q, k)

    # Verifica si hay resultados significativos
    if not resultados:
        return {
            "consulta": q,
            "top_k": k,
            "mensaje": "No se encontró información relevante en el corpus.",
            "disclaimer": "Este asistente no sustituye asesoramiento legal profesional."
        }

    # Genera respuesta usando LLM
    respuesta_generada = generar_respuesta_legal(resultados, q)

    return {
        "consulta": q,
        "top_k": k,
        "resultados": resultados,
        "respuesta_generada": respuesta_generada,
        "disclaimer": "Este asistente no sustituye asesoramiento legal profesional."
    }
