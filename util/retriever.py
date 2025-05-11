from pinecone import Pinecone
import os
from dotenv import load_dotenv
from util.embedder import get_vector_store
from util.metadata_extraction import extract_text_from_pdf, extract_details

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = None


def get_similar_documents(query: str, k: int = 3):
    global pc
    if pc is None:
        pc = Pinecone(api_key=PINECONE_API_KEY)
    vector_store = get_vector_store("case-embeddings", pc)
    if isinstance(query, list):
        query = " ".join(query)
    results = vector_store.similarity_search(query, k=k)
    return results


if __name__ == "__main__":
    pdf_path = (
        "../docs/Dahiben_vs_Arvindbhai_Kalyanji_Bhanusali_Gajra_on_9_July_2020.PDF"
    )
    document_text = extract_text_from_pdf(pdf_path)

    if not document_text.strip():
        print(f"No text found in {pdf_path}")
    try:
        result = extract_details(document_text)
        facts = result.get("facts_for_similar", [])
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

    results = get_similar_documents(facts)

    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:\n{doc.page_content}")
