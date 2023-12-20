from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings


def get_vectorstore(docs: list, persist_directory: str) -> Chroma:
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(),
        persist_directory=persist_directory
    )
    return vectorstore

