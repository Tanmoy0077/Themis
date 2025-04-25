from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from states import ContractState
from util.logger import logger

def review_contract(state: ContractState) -> dict[str, str]:
    prompt = PromptTemplate(
        template="""
You are a meticulous and experienced legal contract reviewer. Your task is to conduct a thorough review of the provided legal document based *strictly* on the given review plan.

**Context:**
*   **Document to Review:** The full text of the legal contract is provided below.
*   **Review Plan:** A specific, step-by-step plan outlining the key areas and aspects to examine has been provided.

**Instructions:**
1.  **Follow the Plan:** Go through each step outlined in the `Review Plan` sequentially.
2.  **Analyze the Document:** For each step in the plan, locate the relevant section(s) or clause(s) in the `Document to Review`.
3.  **Provide Findings:** For each step, clearly state your findings based on your analysis of the document. This should include:
    *   Confirmation of whether the element mentioned in the step exists in the document.
    *   A summary of the relevant contract language.
    *   Identification of any potential issues, risks, ambiguities, deviations from standard practice, or particularly favorable/unfavorable terms related to that step.
    *   If a step asks to assess something (e.g., "Assess fairness"), provide your assessment with justification based *only* on the document text and the instructions in the review step.
4.  **Structure:** Organize your review clearly, referencing each step number from the `Review Plan`.
5.  **Objectivity:** Maintain a neutral and objective tone. Stick to the facts presented in the document and the guidance from the review plan. Do not add steps or review points not mentioned in the plan.

**Review Plan:**
---------------------
{review_steps}
---------------------

**Document to Review:**
---------------------
{document}
---------------------

**Contract Review:**
    """,
        input_variables=["review_steps", "document"],
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", temperature=0.2)

    chain = prompt | llm
    logger.info("Starting Contract Review")
    result = chain.invoke(
        {"review_steps": state.review_steps, "document": state.content}
    )
    logger.info("Contract Review Complete")
    return {"review": result.content}
