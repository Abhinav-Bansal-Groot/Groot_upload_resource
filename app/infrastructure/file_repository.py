import io
import csv
import json
import tempfile
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import (
    TextLoader, PDFPlumberLoader, UnstructuredWordDocumentLoader
)
from langchain_core.documents import Document

# Allowed file extensions
ALLOWED_EXTENSIONS = {".txt", ".csv", ".pdf", ".doc", ".docx", ".json"}

class FileRepository:
    async def load(self, file: UploadFile, ext: str):
        """Load a file into a list of LangChain Document objects."""
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Handle .txt
        if ext == ".txt":
            content = await file.read()
            text = content.decode("utf-8")
            return [Document(page_content=text)]

        # Handle .csv
        elif ext == ".csv":
            content = await file.read()
            reader = csv.reader(io.StringIO(content.decode("utf-8")))
            text = "\n".join([", ".join(row) for row in reader])
            return [Document(page_content=text)]

        # Handle .pdf
        elif ext == ".pdf":
            # Save to a temp file because PDFPlumberLoader needs a path
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name
            return PDFPlumberLoader(tmp_path).load()

        # Handle Word files
        elif ext in [".doc", ".docx"]:
            # Save uploaded file to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                contents = await file.read()
                tmp.write(contents)
                tmp_path = tmp.name

            # Use the temp file path with the loader
            return UnstructuredWordDocumentLoader(tmp_path).load()

        # Handle .json
        elif ext == ".json":
            # Read the file content
            content = await file.read()
            try:
                data = json.loads(content.decode("utf-8"))
            except Exception as e:
                raise ValueError(f"Invalid JSON file: {e}")

            docs = []
            if isinstance(data, list):
                for item in data:
                    sentence = " ".join([f"{k}: {v}" for k, v in item.items()])
                    print("<<< sentence >>> = ", sentence)
                    docs.append(Document(
                        page_content=sentence,
                        metadata=item
                    ))
            else:
                sentence = " ".join([f"{k}: {v}" for k, v in data.items()])
                docs.append(Document(page_content=sentence, metadata=data))
            return docs

