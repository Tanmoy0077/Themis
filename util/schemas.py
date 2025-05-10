from pydantic import BaseModel, Field
from typing import List, Optional

class ClauseDetail(BaseModel):
    """Represents a single extracted clause with analysis."""
    title: str = Field(description="The title or heading of the clause.")
    text: str = Field(description="The full text content of the clause.")
    is_ambiguous: bool = Field(description="Whether the clause text is potentially ambiguous or unclear.")
    ambiguity_reason: Optional[str] = Field(default=None, description="Brief explanation if the clause is marked as ambiguous.")
    is_termination_clause: bool = Field(default=False, description="True if this clause specifically deals with contract termination.")

class ExtractedClauses(BaseModel):
    """Structure containing a list of extracted clauses."""
    clauses: List[ClauseDetail] = Field(description="A list of all distinct clauses extracted from the document.")

class ContractSchema(BaseModel):
    contract_type: str = Field(description="Type of the contract")
    industry: Optional[str] = Field(description="Industry if identifiable")

class ReviewSchema(BaseModel):
    review_steps: list[str] = Field(default_factory=list, description="List of review steps")

class CaseDetail(BaseModel):
    title: str = Field(description="The title or heading of the court case.")
    identifier: str = Field(description="The case number of the court case.")
    summary_for_similar: str = Field(description="Short summary of the court case")
    facts_for_similar: list[str] = Field(description="Important facts on basis of 6 fields from the court case ")