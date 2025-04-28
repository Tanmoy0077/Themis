from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from states import CourtCaseState
from util.logger import logger


def case_facts(state: CourtCaseState) -> dict[str, str]:
    prompt = PromptTemplate(
        template="""

        Task: You are an expert legal document analyst. I will provide you with a full court case document. Your job is to extract structured information from the document based on the following categories. Ensure accuracy and completeness while maintaining a structured format.

        Output Format: Use the format below to organize your response. If a field is missing in the document, return "Not Available".

        1️⃣ Basic Case Details

        Case Title: (Who vs. Who)

        Case Number: (Unique identifier assigned by the court)

        Court Name: (Which court is handling the case)

        Judgment Date: (Date the judgment was issued)

        Judges/Bench: (Names of judges involved)

        Author of Judgment: (If specified)

        Equivalent Citations: (If available)

        2️⃣ Parties Involved

        Appellant(s): (Who filed the appeal)

        Respondent(s): (Who is responding to the appeal)

        Lawyers (if mentioned): (Names of advocates for both sides)

        3️⃣ Nature of Case

        Type of Case: (Civil, Criminal, Constitutional, etc.)

        Acts/Sections Involved: (Legal provisions cited)

        Nature of Dispute: (A short summary of the key legal issue in the case)

        4️⃣ Case Background & Arguments

        Facts of the Case: (Summary of the background events leading to the case)

        Issues Framed: (Key legal questions the court needs to answer)

        Arguments by Appellant: (Main legal and factual arguments)

        Arguments by Respondent: (Defensive arguments against the appeal)

        5️⃣ Court Proceedings & Judgment

        Lower Court Decisions (if applicable): (What the lower court ruled)

        Court’s Observations: (Key reasoning and discussion by the court)

        Final Judgment/Decision: (Outcome—e.g., appeal allowed, dismissed, fine imposed, etc.)

        Compensation Awarded (if applicable): (Details of fines, damages, or penalties)

        Status of the Case: (Pending, Disposed, Referred to another court, etc.)

        6️⃣ Additional Details (If Available)

        Witnesses Mentioned: (Names, if relevant)

        Evidence Discussed: (Key documents, testimonies, forensic reports, etc.)

        Important Precedents Cited: (Any past judgments referred to)

        📌 Output should be structured clearly like a database entry. Do NOT generate extra commentary.



Document from which facts to be extracted:
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
    logger.info("Starting Court Case Facts Generation")
    result = chain.invoke({"document": state.content})
    logger.info("Court Case Facts Generation Complete")
    return {"facts": result.content}
