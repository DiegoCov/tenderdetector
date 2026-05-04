from config import ANTHROPIC_API_KEY, UMBRAL_MATCH, MODELO
from tools.buscar_procesos import buscar_procesos
from tools.calcular_match import calcular_match
from tools.leer_pdf import leer_pdf
from tools.generar_reporte import generar_reporte
from tools.enviar_correo import enviar_correo
import anthropic
from datetime import date

def main():
    print("🚀 TenderDetector iniciando...")
    print(f"   Modelo: {MODELO}")
    print(f"   Umbral de match: {UMBRAL_MATCH}%\n")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print("✅ Conexión con Claude API lista\n")

    with open("perfil_empresa.txt", "r", encoding="utf-8") as f:
        perfil = f.read()

    fecha_hoy = "2025-04-15"
    procesos = buscar_procesos(fecha_hoy)
    print(f"--- Evaluando {len(procesos)} procesos ---\n")

    procesos_relevantes = []

    for p in procesos:
        resultado = calcular_match(p, perfil)
        score = resultado["score"]
        razon = resultado["razon"]
        estado = "✅ PASA" if score >= UMBRAL_MATCH else "❌ descarta"
        print(f"{estado} [{score}] {p['titulo'][:60]}")
        print(f"        {razon}\n")

        if score >= UMBRAL_MATCH:
            p["score"] = score
            procesos_relevantes.append(p)

    print(f"\n--- Fase B: analizando {len(procesos_relevantes)} procesos relevantes ---\n")

    reportes_finales = []

    for p in procesos_relevantes:
        print(f"📄 Leyendo PDF: {p['titulo'][:60]}")
        resultado_pdf = leer_pdf(p["url_pdf"])

        if not resultado_pdf["exito"]:
            print(f"   ⚠️  No se pudo leer el PDF: {resultado_pdf['error']}\n")
            continue

        print(f"   ✅ {resultado_pdf['paginas']} páginas leídas")

        reporte = generar_reporte(resultado_pdf["texto"], perfil, p)
        p["reporte"] = reporte
        reportes_finales.append(p)

        print(f"\n📋 REPORTE — {p['titulo'][:60]}")
        print(reporte)
        print("\n" + "="*60 + "\n")

    print("📧 Enviando correo...")
    enviar_correo(reportes_finales, fecha_hoy)

if __name__ == "__main__":
    main()