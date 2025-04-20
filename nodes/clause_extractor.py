from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from states import ContractState
from typing import Optional
from util.schemas import Clauses


def extract_clauses(state: ContractState) -> Optional[dict[str, str]]:
    parser = PydanticOutputParser(pydantic_object=Clauses)
    prompt = PromptTemplate(
        template="""
    You are a highly skilled legal assistant specialized in contract analysis.
    Your task is to carefully read the following legal document and extract its distinct clauses.
    For each clause identified, define the following:
    1. Clause title (Title of the clause)
    2. Clause text (Text of the clause)
    
    Document:
    {document}
    
    Format Instructions:
    {format_instructions}
    """,
        input_variables=["document"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    chain = prompt | llm | parser
    result = chain.invoke({"document": state.content})
    return result.dict()
