import anthropic
from config import ANTHROPIC_API_KEY, MODELO

def calcular_match(proceso, perfil):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""Eres un asistente que evalúa si una licitación pública peruana es relevante para una empresa.

PERFIL DE LA EMPRESA:
{perfil}

PROCESO DE LICITACIÓN:
Título: {proceso['titulo']}
Descripción: {proceso['descripcion']}
Entidad: {proceso['entidad']}
Monto: S/. {proceso['monto']:,.0f}

Evalúa qué tan relevante es este proceso para la empresa.
Responde ÚNICAMENTE en este formato exacto, sin texto adicional:

SCORE: [número del 0 al 100]
RAZON: [una sola línea explicando el score]"""

    message = client.messages.create(
        model=MODELO,
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )

    respuesta = message.content[0].text.strip()

    try:
        lineas = respuesta.split("\n")
        score = int(lineas[0].replace("SCORE:", "").strip())
        razon = lineas[1].replace("RAZON:", "").strip()
    except:
        score = 0
        razon = "Error al parsear respuesta"

    return {"score": score, "razon": razon}