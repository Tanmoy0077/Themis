from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from states import ContractState
from util.schemas import ReviewSchema
from util.logger import logger

def create_review_plan(state: ContractState) -> dict[str, str]:
    parser = PydanticOutputParser(pydantic_object=ReviewSchema)

    prompt = PromptTemplate(
        template="""
You are a contract review expert AI. Based on the contract type: {contract_type} and the industry: {industry}, generate a review plan that outlines only the most important steps for thoroughly reviewing this type of contract in this context.

**Output:**
Generate only the numbered, step-by-step review plan based on the provided inputs.

**Review Plan for {contract_type} in {industry}:**
{format_instructions}
    """,
        input_variables=["contract_type", "industry"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-preview-04-17", temperature=0.2
    )

    chain = prompt | llm | parser
    logger.info("Starting Review Planning")
    result = chain.invoke(
        {"contract_type": state.contract_type, "industry": state.industry}
    )
    logger.info("Review Planning Complete")
    return {"review_steps": result.review_steps}
