from pydantic import BaseModel, Field
from typing import Optional

class ClauseSchema(BaseModel):
    clause_title: str = Field(..., description="The title of the clause")
    clause_text: str = Field(..., description="The content of the clause")

class Clauses(BaseModel):
    clauses: list[ClauseSchema] = Field(default_factory=list, description="List of clauses")

class ContractSchema(BaseModel):
    contract_type: str = Field(description="Type of the contract")
    industry: Optional[str] = Field(description="Industry if identifiable")