# app/services/qdrant_service.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.core import config

class QdrantService:
    def __init__(self, url: str = config.settings.QDRANT_URL):
        self.client = QdrantClient(url=url)

    def ensure_collection(self, collection_name: str, vector_size: int):
        # Create collection only if it doesn't exist
        collections = self.client.get_collections().collections
        existing = [c.name for c in collections]
        if collection_name not in existing:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )

    def upsert_texts(self, collection_name: str, texts: list[str], embedder):
        # Ensure collection exists before inserting
        vector_size = len(embedder.embed(texts[0]))
        self.ensure_collection(collection_name, vector_size)

        vectors = [embedder.embed(t) for t in texts]
        points = [
            PointStruct(
                id=i,
                vector=vectors[i],
                payload={"text": texts[i]},
            )
            for i in range(len(texts))
        ]

        self.client.upsert(collection_name=collection_name, points=points, wait=True)
        return len(points)
    
    def recreate_collection(self, name: str, vector_size: int):
        self.client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


    def upsert_points(self, collection_name: str, points: list[PointStruct]):
        # Qdrant SDK handles batching on server, but we upsert in caller batches
        self.client.upsert(collection_name=collection_name, points=points, wait=True)


    def search(self, collection_name: str, query_vector: list[float], limit: int = 3):
        return self.client.search(collection_name=collection_name, query_vector=query_vector, limit=limit)

    def upsert_documents(self, collection_name: str, docs: list[str], vectors: list[list[float]]):
        # Ensure collection exists
        if not docs or not vectors:
            return 0
        
        vector_size = len(vectors[0])
        self.ensure_collection(collection_name, vector_size)

        points = [
            PointStruct(
                id=i,
                vector=vectors[i],
                payload={"text": docs[i]},
            )
            for i in range(len(docs))
        ]

        self.client.upsert(collection_name=collection_name, points=points, wait=True)
        return len(points)