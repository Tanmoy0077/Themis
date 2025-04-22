from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from states import ContractState


def summarize_contract(state: ContractState) -> dict[str, str]:
    prompt = PromptTemplate(
        template="""
You are a highly skilled legal assistant specialized in contract analysis and summarization.
Your objective is to create a concise, clear, and accurate summary of the provided legal document.

The summary should be easy to understand for someone who may not have a legal background (e.g., a business stakeholder). Focus on extracting the most critical information.

Please include the following key points in your summary:
1.  **Parties:** Identify the main parties involved in the contract.
2.  **Purpose:** Briefly state the core purpose or subject matter of the agreement (e.g., provision of services, lease of property, employment).
3.  **Key Obligations:** Outline the main responsibilities and duties of each party.
4.  **Term/Duration:** Specify the length of the contract, including start and end dates if mentioned, or if it's ongoing.
5.  **Payment Terms:** Summarize any crucial financial details, like payment amounts, frequency, or conditions (if applicable).
6.  **Governing Law:** Mention the jurisdiction's law that governs the contract, if specified.

Keep the summary objective and neutral. Avoid interpreting ambiguous clauses or offering legal opinions. Aim for clarity and brevity.

Document to Summarize:
---------------------
{document}
---------------------

Summary:
    """,
        input_variables=["document"],
    )
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    chain = prompt | llm
    result = chain.invoke({"document": state.content})
    return {"summary": result.content}
