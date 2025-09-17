from langchain_openai import OpenAIEmbeddings
from app.core import config

class EmbeddingService:
    def __init__(self, model: str | None = None):
        model = model or config.settings.EMBEDDING_MODEL
        self.client = OpenAIEmbeddings(model=model, api_key=config.settings.OPENAI_API_KEY)


    def embed(self, text: str) -> list[float]:
        return self.client.embed_query(text)

    def embed_documents(self, texts: list[str]):
        return self.client.embed_documents(texts)

    def embed_query(self, text: str):
        return self.client.embed_query(text)