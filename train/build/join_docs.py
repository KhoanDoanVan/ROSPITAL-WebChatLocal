import docx
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline
import os

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


doc_files = ["long_english_test.docx"]

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
query = "What was the name of the village where Elias lived?"
docs = vector_db.similarity_search(query, k=1)  # Get top 1 result
retrieved_text = docs[0].page_content

# Load LLM (QA Model)
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

reponse = qa_model(question=query, context=retrieved_text)
answer = reponse["answer"]

print("\n📌 Answer:", answer)