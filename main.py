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
