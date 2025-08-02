from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "").strip()
    print(f"[INCOMING MSG]: {incoming_msg}")

    try:
        response = requests.get("http://127.0.0.1:8000/test_busqueda", params={"q": incoming_msg})
        response.raise_for_status()
        data = response.json()
        print(f"[API RESPONSE]: {data}")

        if data.get("resultados"):
            # Extraemos solo el texto de cada resultado
            textos = [item["texto"] for item in data["resultados"] if "texto" in item]
            resultado_texto = "\n\n".join(textos)
            result = f"🔍 Respuesta legal:\n{resultado_texto}\n\n⚖️ {data.get('disclaimer', '')}"
        else:
            result = data.get("mensaje", "No se encontró información relevante.")
    except Exception as e:
        result = f"❌ Error al conectar con el API: {str(e)}"

    resp = MessagingResponse()
    resp.message(result)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
