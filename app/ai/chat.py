import openai
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from app.functions.config import openai_api_key
from app.ai.documents_loader import pdf_data_loader, web_data_loader
from app.ai.documents_splitting import recursive_character_splitter
from app.ai.vectorstore_enbedding import get_vectorstore
from app.ai.retrieval import get_compression_retriever, pretty_print_docs
from app.functions.config import persist_directory
from app.ai.prompts import system_message_prompt, human_message_prompt
from langchain.prompts import ChatPromptTemplate




openai.api_key = openai_api_key
ll_name = "gpt-3.5-turbo"
persist_directory = persist_directory

def generate_basic_response(message, openai_api_key, ll_name):
    try:
        openai.api_key = openai_api_key
        completion = openai.ChatCompletion.create(
            model = ll_name,
            messages = [ {'role': 'user', 'content': message}],
            temperature = 0
            )

        return completion['choices'][0]['message']['content']
    except Exception as e:
        print("[ERROR] generate_basic_response")
        print("[ERROR] ", e)

def get_db(docs: str):
    r_splitter = recursive_character_splitter(docs=docs, chunk_size=1024, chunk_overlap=256, separators=["\n\n", "\n", "(?<=\. )", " ", ""])
    embeddings = OpenAIEmbeddings()
    db = DocArrayInMemorySearch.from_documents(r_splitter, embeddings)
    return db

def chat_with_docs(query: str, db: DocArrayInMemorySearch):
    llm = OpenAI(temperature=0)

    # memory = ConversationBufferMemory(
    #     memory_key="chat_history",
    #     return_messages=True
    # )

    # vectordb = get_vectorstore(docs=r_splitter, persist_directory=persist_directory)

    compression_retriever = get_compression_retriever(llm=llm, vectorstore=db)
    chat_history = []
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model=ll_name, temperature=0.0),
        chain_type='stuff',
        retriever=compression_retriever,
        combine_docs_chain_kwargs={
            "prompt": ChatPromptTemplate.from_messages([
                system_message_prompt,
                human_message_prompt,
            ]),
        },
    )
    result = qa({"question": query, "chat_history": chat_history})
    print(result)

    return result['answer']