import anthropic
from config import ANTHROPIC_API_KEY, MODELO

def generar_reporte(texto_pdf, perfil, proceso):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""Eres un asistente experto en licitaciones públicas peruanas.
Analiza el siguiente documento de bases de licitación y evalúa si la empresa puede postular.

PERFIL DE LA EMPRESA:
{perfil}

INFORMACIÓN DEL PROCESO:
Título: {proceso['titulo']}
Entidad: {proceso['entidad']}
Monto referencial: S/. {proceso['monto']:,.0f}

TEXTO DE LAS BASES:
{texto_pdf[:6000]}

Genera un reporte con este formato exacto:

MONTO: [monto referencial del contrato]
PLAZO: [plazo de ejecución en días o meses]
EXPERIENCIA: [experiencia mínima requerida]
REQUISITOS: [otros requisitos clave en una línea]
EVALUACION: [si la empresa cumple o no cumple cada punto clave]
VEREDICTO: [POSTULAR / EVALUAR CON CLIENTE / DESCARTAR]
RAZON: [una línea explicando el veredicto]"""

    message = client.messages.create(
        model=MODELO,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text.strip()