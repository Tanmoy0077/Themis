import time
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import pandas as pd

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def create_vector_store(index_name: str, pc: Pinecone):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)
    print("Index created")

def get_vector_store(index_name: str, pc: Pinecone):
    index = pc.Index(index_name)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    return vector_store



if __name__ == "__main__":
    index_name = "case-embeddings"
    pc = Pinecone(api_key=PINECONE_API_KEY)
    CSV_PATH = "../notebooks/data_updated.csv"
    df = pd.read_csv(CSV_PATH)
    documents = []
    for _, row in df.iterrows():
        content = (
            f"Facts: {row['Facts']}"
        )
        
        metadata = {
            "link": row["Link"],
            "title": row["Title"],
            "case_number": row["Identifier"],
            "summary": row["Summary"],
        }

        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)

    vector_store = get_vector_store(index_name, pc)

    vector_store.add_documents(documents)
    print(f"Pushed {len(documents)} document embeddings to vector store.")
