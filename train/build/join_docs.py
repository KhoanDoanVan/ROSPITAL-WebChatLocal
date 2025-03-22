import docx
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline
import os
import ollama

DOCS_FOLDER = os.path.join(os.path.dirname(__file__), "../docs")


def read_docs(file_name):
  file_path = os.path.join(DOCS_FOLDER, file_name)

  if not os.path.exists(file_path):
    raise FileNotFoundError(f"File {file_path} not found")
  
  doc = docx.Document(file_path)
  text = "\n".join([
    p.text for p in doc.paragraphs
      if p.text.strip()
  ])

  return text


doc_files = ["quy_che_benh_vien.docx", "tai_lieu_on_tap.docx"]

documents = [
  read_docs(file) for file in doc_files
]

corpus = "\n".join(documents)


# 🚀 Load embedding model
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_text(corpus)


# 🏛️ Create FAISS vector database
vector_db = FAISS.from_texts(chunks, embedding_model)

# 🔍 Query
# query = "What was the name of the village where Elias lived?"
query = "Điều 6 trong chương III trách nhiệm phạm vi giải quyết công việc và quan hệ cộng tác là gì?"
retrieved_docs = vector_db.similarity_search(query, k=10)  # Get top 10 result


retrieved_text = "\n\n".join([doc.page_content for doc in retrieved_docs])


# Load LLM (QA Model)

# 🧠 Format prompt for LLaMA 3.1
prompt = f"""
You are an AI assistant that answers questions based on retrieved context.

Context:
{retrieved_text}

Question:
{query}

Answer:
"""


# 💡 Send the prompt to LLaMA 3.1
response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])

# 📌 Print response
print("\n📌 Answer:", response["message"]["content"])