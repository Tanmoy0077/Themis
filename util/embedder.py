import time
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


class CaseMetadata(BaseModel):
    case_number: str = Field(..., description="The official case number")
    title: str = Field(..., description="The title of the case")
    summary: str = Field(..., description="A concise summary of the case")
    facts: str = Field(..., description="A list of facts extracted from the case")


def load_document(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError

    loader = PyMuPDFLoader(
        path,
        mode="page",
        images_inner_format="markdown-img",
        images_parser=RapidOCRBlobParser(),
        extract_tables="markdown",
    )

    docs = loader.load()
    content = "\n".join([doc.page_content for doc in docs])

    return content


def extract_case_metadata(text: str) -> dict:
    """
    Extracts case number, title, and summary from legal text using Gemini via Langchain.
    Returns a dictionary with keys: case_number, title, summary and facts.
    """
    parser = PydanticOutputParser(pydantic_object=CaseMetadata)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a legal assistant. Extract the case number, title, facts and a concise summary from the following legal document text. Respond in the specified structured format.",
            ),
            ("human", "{input}\n\n{format_instructions}"),
        ]
    )
    chain = prompt | ChatGoogleGenerativeAI(model="gemini-2.5-pro-exp-03-25") | parser
    result = chain.invoke(
        {"input": text, "format_instructions": parser.get_format_instructions()}
    )
    return result.dict()


def get_vector_store(index_name: str, pc: Pinecone):
    index = pc.Index(index_name)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    return vector_store


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


if __name__ == "__main__":
    index_name = "case-embeddings"
    pc = Pinecone(api_key=PINECONE_API_KEY)
    sample_doc = "docs/Pappu_Deo_Yadav_vs_Naresh_Kumar_on_17_September_2020.PDF"
    text = load_document(sample_doc)
    print("Document loaded")
    metadata = extract_case_metadata(text)
    print("Metadata extracted")
    document = Document(
        page_content=metadata["facts"],
        metadata={
            "case_number": metadata["case_number"],
            "title": metadata["title"],
            "summary": metadata["summary"],
        },
    )
    vector_store = get_vector_store(index_name, pc)
    vector_store.add_documents([document])
    print("Embedding pushed to vector store")
