from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form

from app.infrastructure.chat_repository import ChatRepository

from app.services.retrieval_service import RetrievalService
from app.services.chat_service import ChatService
from app.services.upload_service import UploadService
from app.infrastructure.file_repository import FileRepository

from app.services.qdrant_service import QdrantService
from app.services.llm import LLMService
from app.services.URLService import URLService
from app.services.embeddings import EmbeddingService

from .schemas import ChatRequest, ChatResponse
import json
import os

router = APIRouter(prefix="/api")


def get_services():
    qdrant = QdrantService()
    embedder = EmbeddingService()
    llm = LLMService()

    retr = RetrievalService(qdrant, embedder)
    chat_service = ChatService(retr, llm)
    chat_repo = ChatRepository(chat_service)   
    return {"qdrant": qdrant, "embedder": embedder, "retr": retr, "chat_service": chat_service, "chat_repo": chat_repo}



@router.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest):
    services = get_services()
    res = services["chat_repo"].handle_chat(body.question)
    return {"answer": res["answer"]}


@router.post("/embed-resource")
async def upload_resource(
    file: UploadFile = File(...),
    collection_name: str = Form("resource_collection")
):
    services = get_services()
    qdrant = services["qdrant"]
    embedder = services["embedder"]
    file_repo = FileRepository()

    upload_service = UploadService(qdrant, embedder, file_repo)
    result = await upload_service.upload_file(file, collection_name)
    return result

@router.post("/embed-website-text")
async def embed_url(url: str = Form(...), collection_name: str = Form("url_collection")):
    services = get_services()
    qdrant = services["qdrant"]
    embedder = services["embedder"]
    url_service = URLService()

    try:
        text = url_service.extract_text(url)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    texts = [text]  # could later split
    count = qdrant.upsert_texts(collection_name, texts, embedder)
    return {"status": "success", "points_added": count, "source": url}

