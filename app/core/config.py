from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGO_DB = os.getenv("DB_NAME")
    QDRANT_URL = os.getenv("QDRANT_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "3072"))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "256"))
    # COLLECTIONS = [c.strip() for c in os.getenv("COLLECTIONS", "Careers,ServicesOffereds,DirectorsInfo").split(",")]
    # COLLECTIONS = os.getenv("COLLECTIO", "json")
    PROJECT_NAME: str = "Grootbot"  # chatbot name
    BOT_ROLE: str = "AI assistant"  # role/identity
    BOT_INSTRUCTIONS : str = "You are a helpful assistant. Use the following context to answer the question.\n\n"
    GPT_MODEL = os.getenv("GPT_MODEL")

    META_QUESTIONS = [
    "what is your name",
    "who are you",
    "whom am i talking with",
    "who created you",
    "tell me about yourself"
    ]

settings = Settings()