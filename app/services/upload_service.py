import os
from fastapi import UploadFile
from app.infrastructure.file_repository import FileRepository
from app.services.qdrant_service import QdrantService
from app.services.embeddings import EmbeddingService

class UploadService:
    def __init__(self, qdrant: QdrantService, embedder: EmbeddingService, file_repo: FileRepository):
        self.qdrant = qdrant
        self.embedder = embedder
        self.file_repo = file_repo

    async def upload_file(self, file: UploadFile, collection_name: str):
        # Detect extension
        _, ext = os.path.splitext(file.filename.lower())

        # Load into documents using repo
        docs = await self.file_repo.load(file, ext)

        # Embed
        vectors = self.embedder.embed_documents([doc.page_content for doc in docs])

        # Store in Qdrant
        self.qdrant.upsert_documents(collection_name, docs, vectors)
        return {"message": f"✅ {len(docs)} chunks stored in {collection_name}"}
