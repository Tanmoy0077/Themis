from typing import Optional
from pydantic import BaseModel

class ContractState(BaseModel):
    document_path: Optional[str] = None
    contract_type: Optional[str] = None
    industry: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    clauses: Optional[list[dict[str, str]]] = None
    review_steps: Optional[list[str]] = None