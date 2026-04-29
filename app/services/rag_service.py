import os
import shutil
from typing import List
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from GeekyAnts.app.core.config import settings

# Setup Data Directories
DATA_DIR = os.path.join(os.getcwd(), "data")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=self.embeddings)
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", anthropic_api_key=settings.ANTHROPIC_API_KEY, temperature=0)

    async def ingest_pdf(self, file: UploadFile) -> int:
        """
        Save the uploaded PDF, load it, split it, and store embeddings in Chroma.
        Returns the number of chunks added.
        """
        file_path = os.path.join(UPLOADS_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. Load
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # 2. Chunk
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )
        chunks = text_splitter.split_documents(docs)
        
        # 3. Embed and Store
        self.vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=self.embeddings, 
            persist_directory=CHROMA_DIR
        )
        
        return len(chunks)

    def query(self, question: str) -> str:
        """
        Query the vector store and generate an answer based on the context.
        """
        retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        
        # Get relevant documents
        docs = retriever.invoke(question)
        
        # Build context from documents
        context = "\n".join([doc.page_content for doc in docs])
        
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Use three sentences maximum and keep the answer concise.\n\n"
            f"Context:\n{context}"
        )
        
        messages = [HumanMessage(content=system_prompt + f"\n\nQuestion: {question}")]
        
        response = self.llm.invoke(messages)
        return response.content

rag_service = RAGService()
