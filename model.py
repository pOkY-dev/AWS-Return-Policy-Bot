from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_nomic.embeddings import NomicEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict, List
from langchain.schema import Document

with open('amazon_return_policy.txt', 'r', encoding='utf-8') as file:
    text = file.read()

docs = [Document(page_content=text, metadata={})]

# Adjust chunk size and overlap for better coverage
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=150,  
    chunk_overlap=50  
)


# Split the documents into chunks
doc_splits = []
for doc in docs:
    splits = text_splitter.split_text(doc.page_content)  
    for split in splits:
        doc_splits.append(Document(page_content=split, metadata=doc.metadata))  # Create new Document objects

# Add the document chunks to the "vector store" using NomicEmbeddings
vectorstore = SKLearnVectorStore.from_documents(
    documents=doc_splits,
    embedding=NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")
)

retriever = vectorstore.as_retriever(k=6)

prompt = PromptTemplate(
    template="""You are an assistant for question-answering tasks. 
                Use the information from the documents provided below to answer the question as precisely as possible. 
                Directly cite relevant portions of the documents where applicable:
                Question: {question} 
                Documents: {documents} 
                Answer: """,
    input_variables=["question", "documents"],
)

llm = ChatOllama(model="llama2", temperature=0)
rag_chain = prompt | llm | StrOutputParser()

# Define the Graph State
class GraphState(TypedDict):
    question: str
    generation: str
    search: str
    documents: List[str]
    steps: List[str]

def retrieve(state):
    question = state["question"]
    documents = retriever.invoke(question)
    steps = state["steps"]
    steps.append("retrieve_documents")
    return {"documents": documents, "question": question, "steps": steps}

def generate(state):
    question = state["question"]
    documents = state["documents"]
    generation = rag_chain.invoke({"documents": documents, "question": question})
    steps = state["steps"]
    steps.append("generate_answer")
    return {
        "documents": documents,
        "question": question,
        "generation": generation,
        "steps": steps,
    }

# Build the workflow graph
workflow = StateGraph(GraphState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

# Compile the graph and also export the rag_chain
custom_graph = workflow.compile()
