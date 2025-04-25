from states import ContractState
from util.embedder import load_document
from util.logger import logger

def document_loader(state: ContractState) -> str:
    logger.info("Loading Document")
    content = load_document(state.document_path)
    logger.info("Document Loaded")
    return {"content": content}
