from fastapi import FastAPI
from app.api.routes import router as api_router


app = FastAPI(title="RAG FastAPI (Clean Architecture)")
app.include_router(api_router)


# # main.py
# from fastapi import FastAPI, File, UploadFile, Query
# from qdrant_service import client, COLLECTION_NAME
# from embed_service import get_embedding
# from url_service import extract_text_from_url
# import uuid

# app = FastAPI()

# @app.post("/upload-text/")
# async def upload_text(file: UploadFile = File(...)):
#     content = await file.read()
#     text = content.decode("utf-8")

#     # Split into smaller chunks if needed (optional)
#     texts = [text]  # You can use LangChain's text splitter here

#     points = []
#     for t in texts:
#         vector = get_embedding(t)
#         points.append({
#             "id": str(uuid.uuid4()),
#             "vector": vector,
#             "payload": {"text": t}
#         })

#     # Upsert into Qdrant
#     client.upsert(collection_name=COLLECTION_NAME, points=points)
#     return {"status": "success", "points_added": len(points)}


# @app.post("/embed-url/")
# async def embed_url(url: str = Query(..., description="The URL to fetch and embed")):
#     try:
#         text = extract_text_from_url(url)
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

#     # Optional: split into chunks if text is long
#     texts = [text]  # For now we embed whole text at once

#     points = []
#     for t in texts:
#         vector = get_embedding(t)
#         points.append({
#             "id": str(uuid.uuid4()),
#             "vector": vector,
#             "payload": {"text": t, "source": url}
#         })

#     client.upsert(collection_name=COLLECTION_NAME, points=points)
#     return {"status": "success", "points_added": len(points)}