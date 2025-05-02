from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from states import ContractState
from util.schemas import ExtractedClauses
from util.logger import logger


def extract_clauses(state: ContractState):
    parser = PydanticOutputParser(pydantic_object=ExtractedClauses)
    prompt = PromptTemplate(
        template="""
    You are a legal assistant AI. Your task is to analyze the following legal contract and extract the key clauses.
For each key clause identified, please provide the following information:
1.  **Clause Title:** The original title or heading of the clause as it appears in the document. If no title exists, infer a concise one (e.g., "Confidentiality Obligations").
2.  **Clause Text:** Summary of the clause text.
3.  **Ambiguity Check:** Assess if the clause's language is potentially ambiguous, unclear, or open to multiple interpretations. Set `is_ambiguous` to true or false.
4.  **Ambiguity Reason:** If `is_ambiguous` is true, provide a brief explanation of *why* it might be considered ambiguous. If false, this can be omitted or null.
5.  **Termination Clause Identification:** Determine if this specific clause primarily deals with the conditions, procedures, or consequences of terminating the contract. Set `is_termination_clause` to true if it is, otherwise false.

**Document:**
---------------------
{document}
---------------------

**Format Instructions:**
{format_instructions}

Ensure your output strictly follows the format instructions. Analyze each clause independently for ambiguity and its relevance to termination.
    """,
        input_variables=["document"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", temperature=0.2)
    chain = prompt | llm | parser
    logger.info("Starting Clause Extraction")
    result = chain.invoke({"document": state.content})
    logger.info("Clause Extraction Complete")
    return {"clauses": result.clauses}
