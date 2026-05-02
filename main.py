from config import ANTHROPIC_API_KEY, UMBRAL_MATCH, MODELO
from tools.buscar_procesos import buscar_procesos
from tools.calcular_match import calcular_match
import anthropic

def main():
    print("🚀 TenderDetector iniciando...")
    print(f"   Modelo: {MODELO}")
    print(f"   Umbral de match: {UMBRAL_MATCH}%\n")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print("✅ Conexión con Claude API lista\n")

    with open("perfil_empresa.txt", "r", encoding="utf-8") as f:
        perfil = f.read()

    procesos = buscar_procesos("2025-03-10")
    print(f"--- Evaluando {len(procesos)} procesos ---\n")

    for p in procesos:
        resultado = calcular_match(p, perfil)
        score = resultado["score"]
        razon = resultado["razon"]
        estado = "✅ PASA" if score >= UMBRAL_MATCH else "❌ descarta"
        print(f"{estado} [{score}] {p['titulo'][:60]}")
        print(f"        {razon}\n")

if __name__ == "__main__":
    main()