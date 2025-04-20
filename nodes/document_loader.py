from states import ContractState
from util.embedder import load_document


def document_loader(state: ContractState) -> str:
    content = load_document(state.document_path)
    return {"content": content}
