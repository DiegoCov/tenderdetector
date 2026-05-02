from config import ANTHROPIC_API_KEY, UMBRAL_MATCH, MODELO
import anthropic

def main():
    print("🚀 TenderDetector iniciando...")
    print(f"   Modelo: {MODELO}")
    print(f"   Umbral de match: {UMBRAL_MATCH}%")
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    print("✅ Conexión con Claude API lista")
    print("⏳ Herramientas del agente: en construcción")

if __name__ == "__main__":
    main()