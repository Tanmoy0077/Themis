from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from states import ContractState
from util.logger import logger


def review_contract(state: ContractState) -> dict[str, str]:
    prompt = PromptTemplate(
        template="""
You are a contract review assistant. Your task is to review a contract based on the following review steps:

{review_steps}

Analyze the contract carefully according to each step. For every step, provide a concise summary in clear, non-legal language that helps a non-lawyer understand the key points, risks, or concerns. Focus on practical implications, unclear terms, or anything that might require attention or negotiation.

**Document to Review:**
---------------------
{document}
---------------------

**Contract Review:**
    """,
        input_variables=["review_steps", "document"],
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-preview-04-17", temperature=0.2
    )

    chain = prompt | llm
    logger.info("Starting Contract Review")
    result = chain.invoke(
        {"review_steps": state.review_steps, "document": state.content}
    )
    logger.info("Contract Review Complete")
    return {"review": result.content}
