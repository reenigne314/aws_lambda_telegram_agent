from loguru import logger

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from telegram_agent_aws.infrastructure.qdrant_utils import get_qdrant_client
from telegram_agent_aws.config import settings


def generate_split_documents():
    loader = PyPDFLoader("./data/karan_full_biography.pdf")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    docs = loader.load()
    all_splits = text_splitter.split_documents(docs)

    return all_splits


def index_documents():
    all_splits = generate_split_documents()
    embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY)

    vector_store = QdrantVectorStore(
        client=get_qdrant_client(),
        collection_name="telegram_agent_aws_collection",
        embedding=embeddings,
    )

    vector_store.add_documents(all_splits)

    logger.info("Documents indexed successfully.")
