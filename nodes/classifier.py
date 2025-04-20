from states import ContractState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from typing import Optional
from util.schemas import ContractSchema


def classify_contract(state: ContractState) -> Optional[dict[str, str]]:
    parser = PydanticOutputParser(pydantic_object=ContractSchema)
    prompt = PromptTemplate(
        template="""
    You are a legal assistant specialized in contract analysis.
    Your task is to identify the following:
    1. Contract type (e.g., Employment, NDA, License Agreement).
    2. Industry (if clear from the context otherwise provide "Not specified").
    
    Document:
    {document}
    
    Format Instructions:
    {format_instructions}
    """,
        input_variables=["document"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    chain = prompt | llm | parser

    result = chain.invoke({"document": state.content})
    return result.dict()
