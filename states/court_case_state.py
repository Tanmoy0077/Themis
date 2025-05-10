from typing import Optional
from pydantic import BaseModel


class CourtCaseState(BaseModel):
    document_path: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    facts: Optional[str] = None
 
