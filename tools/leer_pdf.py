import requests
import pdfplumber
import io
from config import MAX_PAGINAS_PDF

def leer_pdf(url):
    if not url:
        return {"exito": False, "texto": "", "paginas": 0, "error": "URL vacía"}

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
    except Exception as e:
        return {"exito": False, "texto": "", "paginas": 0, "error": f"Error al descargar: {e}"}

    try:
        pdf_bytes = io.BytesIO(response.content)
        texto_paginas = []

        with pdfplumber.open(pdf_bytes) as pdf:
            total_paginas = len(pdf.pages)
            paginas_a_leer = min(total_paginas, MAX_PAGINAS_PDF)

            for i in range(paginas_a_leer):
                texto = pdf.pages[i].extract_text()
                if texto:
                    texto_paginas.append(texto)

        texto_completo = "\n\n".join(texto_paginas)

        return {
            "exito": True,
            "texto": texto_completo,
            "paginas": paginas_a_leer,
            "error": ""
        }

    except Exception as e:
        return {"exito": False, "texto": "", "paginas": 0, "error": f"Error al leer PDF: {e}"}