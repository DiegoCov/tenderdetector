import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
UMBRAL_MATCH = 30
MODELO = "claude-sonnet-4-5"
MAX_PAGINAS_PDF = 15