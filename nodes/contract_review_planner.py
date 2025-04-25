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
You are a highly skilled legal assistant specialized in contract review and analysis.

Your objective is to generate a detailed, step-by-step contract review plan tailored to the specific context provided.

**Context:**
*   **Contract Type:** {contract_type}
*   **Industry:** {industry}

**Task:**
Based on the contract type (`{contract_type}`) and industry (`{industry}`) provided above, create a sequential and actionable review plan. This plan should guide a reviewer (e.g., a lawyer, paralegal, or contract manager) through the process of thoroughly examining the contract document.

**Instructions:**
1.  **Sequential Steps:** Present the plan as a numbered list of clear, logical steps, starting from initial preparation to final assessment.
2.  **Actionable Language:** Phrase each step using action verbs (e.g., "Identify," "Verify," "Analyze," "Assess," "Review").
3.  **Contextual Relevance:** Tailor the steps specifically considering the nuances, common clauses, potential risks, and regulatory landscape typical for the given `{contract_type}` within the `{industry}`. For example, a Software License Agreement in the Healthcare industry will have different points of focus than an Employment Agreement in the Retail industry.
4.  **Comprehensive Coverage:** Ensure the plan encourages review of essential contract components, including (but not limited to):
    *   Parties and Definitions
    *   Scope of Work / Subject Matter
    *   Term and Termination
    *   Payment Obligations / Financial Terms
    *   Representations and Warranties
    *   Confidentiality
    *   Intellectual Property (if applicable)
    *   Indemnification and Limitation of Liability
    *   Data Privacy and Security (especially relevant for certain industries/types)
    *   Compliance Requirements (specific to the industry)
    *   Dispute Resolution
    *   Governing Law
5.  **Risk Focus:** Include steps specifically aimed at identifying potential risks, ambiguities, deviations from standard practice, or unfavorable terms for a hypothetical client (or from a neutral perspective).
6.  **Clarity and Conciseness:** Keep the language clear and to the point.

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
