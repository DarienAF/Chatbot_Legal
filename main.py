from fastapi import FastAPI, Form, Query
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from utils.search_engine import BuscadorLegal
from collections import Counter
# from utils.twilio_utils import send_message  # función que envía mensajes via Twilio

# Instancia de la aplicacion web
app = FastAPI(title="LegalBot Semántico")

# Instancia del buscador al iniciar
buscador = BuscadorLegal(corpus_path='legal_corpus')

@app.get("/")
def root():
    return {"mensaje": "LegalBot Semántico activo"}

@app.post("/message")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...)
):
    resultados = buscador.buscar(Body, k=5)
    umbral = 0.8

    relevantes = [r for r in resultados if r["distancia"] <= umbral]

    if not relevantes:
        respuesta = (
            "⚖️ LegalBot:\n\n"
            "No se encontró información relevante sobre tu consulta. "
            "Intentá reformularla.\n\n"
            "🛑 Este asistente no sustituye asesoramiento legal profesional."
        )
    else:
        # 1. Armar partes del mensaje
        partes = [f"• {r['texto']}" for r in relevantes]

        # 2. Contar ocurrencias por fuente
        fuentes = [r["fuente"] for r in relevantes]
        fuente_dominante = Counter(fuentes).most_common(1)[0][0]  

        # 3. Diccionario de enlaces por fuente
        enlaces_fuentes = {
            "laboral.md": "https://www.mtss.go.cr/",
            "consumo.md": "https://www.meic.go.cr/",
            "alquiler.md": "https://www.mivah.go.cr/Nosotros_Quienes_Somos.shtml"
        }

        # 4. Obtener el enlace segun la fuente dominante
        enlace_extra = enlaces_fuentes.get(fuente_dominante, None)

        # 5. Armar respuesta final
        respuesta = (
            "⚖️ LegalBot:\n\n" +
            "\n\n".join(partes) +
            "\n\n"
        )

        if enlace_extra:
            respuesta += f"🔗 Más información relacionada: {enlace_extra}\n\n"

        respuesta += "🛑 Este asistente no sustituye asesoramiento legal profesional."

    twiml = MessagingResponse()
    twiml.message(respuesta)
    return PlainTextResponse(str(twiml), media_type="application/xml")


# Webhook para WhatsApp (POST desde Twilio)
"""
@app.post("/message")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...)
):
    # Procesar consulta y obtener resultados
    resultados = buscador.buscar(Body, k=3)

    if not resultados:
        respuesta = (
            "No se encontró información relevante. "
            "Intentá reformular tu consulta."
        )
    else:
        items = [f"• {r['texto']} (Fuente: {r['fuente']})" for r in resultados]
        respuesta = "\n\n".join(items)

    # Enriquecer mensaje con encabezado opcional
    header = "LegalBot:\n\n"
    full_message = header + respuesta

    # TwiML para responder al webhook Twilio
    twiml = MessagingResponse()
    twiml.message(full_message)

    # Además, usá tu función utilitaria para enviar por la API REST, si preferís:
    # send_message(to_number=From, body_text=full_message)

    return PlainTextResponse(str(twiml), media_type="application/xml")
"""

"""
@app.get("/test_busqueda")
def test_busqueda(
    q: str = Query(..., description="Consulta legal para buscar en el corpus"),
    k: int = Query(3, description="Número de fragmentos que se retornarán")
):
    
   # Endpoint de prueba: recibe una consulta 'q', busca en el corpus legal
   # y genera una respuesta en lenguaje natural.
   
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
"""