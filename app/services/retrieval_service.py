from langchain_core.documents import Document


class RetrievalService:
    def __init__(self, qdrant_service, embedder):
        self.qdrant = qdrant_service
        self.embedder = embedder

    # def retrieve(self, query: str, top_k: int = 30) -> list[Document]:
    #     qvec = self.embedder.embed(query)
    #     docs = []
    #     for coll in [c.strip().lower() + "_collection" for c in config.settings.COLLECTIONS.split(",")]:
    #         results = self.qdrant.search(coll, qvec, limit=top_k)
    #         print(">>>> results >>>",results)
    #         for r in results:
    #             payload = r.payload or {}
    #             text = " ".join([str(v) for v in payload.values() if isinstance(v, str)])
    #             docs.append(Document(page_content=text, metadata={"source": coll}))
    #     return docs

    def retrieve(self, query: str, top_k: int = 3) -> list[Document]:
        qvec = self.embedder.embed(query)
        docs = []
        for coll in self.qdrant.list_collections():
            results = self.qdrant.search(coll, qvec, limit=top_k)
            for r in results:
                payload = r.payload or {}
                text = " ".join([str(v) for v in payload.values() if isinstance(v, str)])
                docs.append(Document(page_content=text, metadata={"source": coll}))
        return docs