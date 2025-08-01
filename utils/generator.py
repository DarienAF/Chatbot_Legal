import requests
import os

# Modelo sugerido: llama-3-70b-instruct (gratis y potente)
MODEL_NAME = "meta-llama/Meta-Llama-3-70B-Instruct"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  # Recomendado: usar variable de entorno

def generar_respuesta_legal(fragmentos: list[dict], pregunta: str) -> str:
    """
    Genera una respuesta legal usando los fragmentos obtenidos y la consulta original.
    """
    # Construye contexto con los textos relevantes
    contexto = "\n\n".join([f"- {frag['texto']}" for frag in fragmentos])

    # Prompt claro para el modelo
    prompt = (
        "Eres un asistente legal que responde preguntas con base en normativa. "
        "No inventes información y responde únicamente si tienes evidencia en el contexto proporcionado.\n\n"
        f"Contexto legal:\n{contexto}\n\n"
        f"Pregunta del usuario: {pregunta}\n\n"
        "Respuesta clara y precisa:"
    )

    # Payload para la API
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Eres un asistente legal útil y confiable."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"[ERROR al generar respuesta legal]: {str(e)}"