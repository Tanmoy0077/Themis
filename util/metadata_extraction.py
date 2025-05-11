from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import pandas as pd
from tqdm import tqdm
import os
import fitz
from util.schemas import CaseDetail
from util.logger import logger

PDF_FOLDER = "../docs"
CSV_FILE = "../notebooks/cleaned_downloaded_pdfs_log.csv"


def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Failed to extract text from {pdf_path}: {e}")
        return ""


def extract_details(document_text):
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
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-preview-04-17", temperature=0.2
    )
    chain = prompt | llm | parser
    logger.info("Starting Case Details Extraction")
    result = chain.invoke({"document": document_text})
    logger.info("Case Details Extraction Complete")
    return result.dict()


# pdf="docs\Dahiben_vs_Arvindbhai_Kalyanji_Bhanusali_Gajra_on_9_July_2020.PDF"
# result_dict = extract_details(pdf)

# title = result_dict.get("title", "Not Available")
# identifier = result_dict.get("identifier", "Not Available")
# summary = result_dict.get("summary_for_similar", "Not Available")
# facts = result_dict.get("facts_for_similar", [])

# print("Title:", title)
# print("Identifier:", identifier)
# print("Summary:", summary)
# print("Facts:")
# for fact in facts:
#     print("-", fact)

if __name__ == "__main__":
    df = pd.read_csv(CSV_FILE)
    # print(os.listdir(PDF_FOLDER))

    for col in ["Title", "Identifier", "Summary", "Facts"]:
        if col not in df.columns:
            df[col] = ""

    for i, row in tqdm(df.iterrows(), total=len(df)):
        pdf_name = row["PDF Path"]
        pdf_path = os.path.join(PDF_FOLDER, pdf_name)

        if not os.path.exists(pdf_path):
            print(f"File not found: {pdf_path}")
            continue

        document_text = extract_text_from_pdf(pdf_path)
        if not document_text.strip():
            print(f"No text found in {pdf_name}")
            continue

        try:
            result = extract_details(document_text)
            df.at[i, "Title"] = result.get("title", "Not Available")
            df.at[i, "Identifier"] = result.get("identifier", "Not Available")
            df.at[i, "Summary"] = result.get("summary_for_similar", "Not Available")
            df.at[i, "Facts"] = " | ".join(result.get("facts_for_similar", []))
        except Exception as e:
            print(f"Error processing {pdf_name}: {e}")

    df.to_csv("data_updated.csv", index=False)
    print("Extraction complete. Saved to data_updated.csv")
