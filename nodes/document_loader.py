from util.logger import logger
from util.embedder import load_document
from pydantic import BaseModel

def document_loader(state: BaseModel) -> str:
    logger.info("Loading Document")
    content = load_document(state.document_path)
    logger.info("Document Loaded")
    return {"content": content}
