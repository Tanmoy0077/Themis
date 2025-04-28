from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from states import CourtCaseState
from util.logger import logger


def summarize_case(state: CourtCaseState) -> dict[str, str]:
    prompt = PromptTemplate(
        template="""

        You are an expert legal document analyst. I will provide you with a full court case document. Your job is to provide a brief summary of the court case capturing its main essence, including the basic case details in a narrative format, followed by key information about the parties involved.

        The summary should include:

        A paragraph that highlights main essence of the court case.

        1️⃣ Basic Case Details
        A paragraph on this that includes details like Case Title (Who vs. Who), Case Number (Unique identifier assigned by the court), Court Name (Which court is handling the case), Type of Case (Civil, Criminal, Constitutional, etc.), Judgment Date (Date the judgment was issued), Judges/Bench (Names of judges involved), Author of Judgment (If specified), Equivalent Citations (If available)

        2️⃣ Parties Involved
        Appellant(s): (Who filed the appeal)
        Respondent(s): (Who is responding to the appeal)
        Lawyers (if mentioned): (Names of advocates for both sides)

        Add a concluding paragraph on the court case


        Ensure the basic case details are included in a cohesive, paragraph-like format, while keeping the parties of the case clear in point form.

Document to Summarize:
---------------------
{document}
---------------------

Summary:
    """,
        input_variables=["document"],
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-preview-04-17", temperature=0.2
    )
    chain = prompt | llm
    logger.info("Starting Court Case Summarization")
    result = chain.invoke({"document": state.content})
    logger.info("Court Case Summarization Complete")
    return {"summary": result.content}
