from langchain.llms import OpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor


def pretty_print_docs(docs : list):
    print(f"\n{'-' * 100}\n".join([f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]))


def get_compression_retriever(llm: OpenAI, vectorstore=None) -> ContextualCompressionRetriever:
    compresor = LLMChainExtractor.from_llm(llm=llm)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compresor,
        base_retriever=vectorstore.as_retriever(search_type = 'mmr')
    )

    return compression_retriever

