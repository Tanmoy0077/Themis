from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from states import ContractState
import os


def load_document(state: ContractState) -> str:
    if not os.path.exists(state.document_path):
        raise FileNotFoundError

    loader = PyMuPDFLoader(
        state.document_path,
        mode="page",
        images_inner_format="markdown-img",
        images_parser=RapidOCRBlobParser(),
        extract_tables="markdown",
    )

    docs = loader.load()
    content = "\n".join([doc.page_content for doc in docs])
    
    return {"content": content}
