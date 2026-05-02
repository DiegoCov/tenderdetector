from config import ANTHROPIC_API_KEY, UMBRAL_MATCH, MODELO
from tools.buscar_procesos import buscar_procesos
import anthropic

def main():
    print("🚀 TenderDetector iniciando...")
    print(f"   Modelo: {MODELO}")
    print(f"   Umbral de match: {UMBRAL_MATCH}%")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print("✅ Conexión con Claude API lista\n")

    procesos = buscar_procesos("2025-04-28")
    for p in procesos[:3]:
        print(f"📄 {p['titulo']}")
        print(f"   Entidad: {p['entidad']}")
        print(f"   Monto: S/. {p['monto']:,.0f}")
        print(f"   OCID: {p['ocid']}\n")

if __name__ == "__main__":
    main()