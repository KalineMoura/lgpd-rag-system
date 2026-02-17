from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import re


def infer_doc_type(filename: str) -> str:
    name = filename.lower()
    if "lgpd" in name:
        return "LGPD"
    return "Desconhecido"


def extract_article(text: str):
    """
    Best-effort extraction of legal article
    """
    match = re.search(r"(Art\.?\s*\d+[º°]?)", text)
    if match:
        return match.group(1)
    return None


def extract_pdf_text(pdfs):
    """
    Extract text from PDF documents and enrich metadata
    """
    docs = []

    for pdf in pdfs:
        pdf_path = os.path.join("docs", pdf)
        loaded_docs = PyPDFLoader(pdf_path).load()

        doc_type = infer_doc_type(pdf)

        for doc in loaded_docs:
            # Metadata básica
            doc.metadata["filename"] = pdf
            doc.metadata["doc_type"] = doc_type

            # Metadata opcional: artigo
            article = extract_article(doc.page_content)
            if article:
                doc.metadata["article"] = article

        docs.extend(loaded_docs)

    return docs


def get_text_chunks(docs):
    """
    Split text into chunks

    Parameters:
    - docs (list): List of text documents

    Returns:
    - chunks: List of text chunks
    """
    # Chunk size is configured to be an approximation to the model limit of 2048 tokens
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=300, separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(docs)
    return chunks


def get_vectorstore(pdfs, from_session_state=False):
    load_dotenv()

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Caso 1: carregar DB existente
    if from_session_state and os.path.exists("Vector_DB - Documents"):
        return Chroma(
            persist_directory="Vector_DB - Documents", embedding_function=embedding
        )

    # Caso 2: criar DB do zero
    docs = extract_pdf_text(pdfs)
    chunks = get_text_chunks(docs)

    print("\n=== DEBUG METADATA (primeiros 3 chunks) ===")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i}")
        print("Metadata:", chunk.metadata)
        print("Preview:", chunk.page_content[:200])

    if not chunks:
        raise ValueError("No text chunks could be created from the PDF.")

    return Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="Vector_DB - Documents",
    )
