from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from states import ContractState
from util.schemas import ReviewSchema


def create_review_plan(state: ContractState) -> dict[str, str]:
    parser = PydanticOutputParser(pydantic_object=ReviewSchema)

    prompt = PromptTemplate(
        template="""
    You are a highly skilled legal assistant specialized in contract review.
    Your task is to create contract review plan for a {contract_type} contract with {industry} industry.
    ** Generate the steps sequentially**
    """,
        input_variables=["contract_type", "industry"],
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", temperature=0.2
    ).with_structured_output(parser)

    chain = prompt | llm

    result = chain.invoke(
        {"contract_type": state.contract_type, "industry": state.industry}
    )
    return {"review_steps": result.review_steps}
