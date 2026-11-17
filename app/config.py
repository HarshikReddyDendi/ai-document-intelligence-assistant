
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-20b"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")
