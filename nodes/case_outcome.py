from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from states import CourtCaseState
from util.schemas import CaseDetail
from util.logger import logger


def extract_details(state: CourtCaseState):
    parser = PydanticOutputParser(pydantic_object=CaseDetail)
    prompt = PromptTemplate(
        template="""
    You are a legal assistant AI. Your task is to analyze the following legal court case and extract the details mentioned below.
For the court case, please provide the following information:
1.  **Case Title:** The original title or heading of the court case as it appears in the document. (Who vs. Who)
2.  **Case Number:** Unique identifier assigned by the court.
3.  **Summary:** Explain the essence of the entire case in 2-3 lines mainly discussing about the issue it involves.
4.  **Important details:** Give the following details exactly how it is mentioned. If any field is not clearly available, return "Not Available".
    4.1 **Nature of Case:** Type of Case: (Civil, Criminal, Constitutional, Environmental, Company Law, etc.), Acts/Sections Involved: (List all major acts and legal sections cited), Nature of Dispute: (One-line summary of the dispute: e.g., "Winding up petition for unpaid debt", "Murder trial", "Breach of contract")
    4.2 **Relevant Acts / Sections:** (List all important legal acts and sections cited in the case, e.g., IPC 302, Companies Act 1956, IBC 2016.)
    4.3 **Issues Framed:** (List the key legal issues/questions that the court considered or answered.)
    4.4 **Facts of the Case:** (Summarize the essential background and legal core and events that led to the legal dispute — maximum 5-6 lines.)
    4.5 **Arguments Presented (Optional):** (Summary of main legal arguments if they clearly influence the nature of the case)
    4.6 **Judgment Outcome:** (State the final decision — e.g., "Appeal allowed", "Case dismissed", "Compensation awarded", "Winding up ordered", etc.)



**Document:**
---------------------
{document}
---------------------

**Format Instructions:**
{format_instructions}

Ensure your output strictly follows the format instructions. Analyze each court case to provide accurate information.
    """,
        input_variables=["document"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", temperature=0.2)
    chain = prompt | llm | parser
    logger.info("Starting Case Details Extraction")
    result = chain.invoke({"document": state.content})
    logger.info("Case Details Extraction Complete")
    return result.dict()

