import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.4"))

CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_data")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "client_knowledge")
