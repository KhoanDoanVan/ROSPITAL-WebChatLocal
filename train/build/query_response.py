import ollama
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

# 🔥 Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Call FAISS
faiss_path = os.path.abspath("faiss_index")

# Load FAISS with safe rule
print(f"📌 Loading FAISS index from: {faiss_path}")
vector_db = FAISS.load_local(faiss_path, embeddings=embedding_model, allow_dangerous_deserialization=True)

# ✅ Debug: Check indexs in FAISS
if hasattr(vector_db, "index") and vector_db.index.ntotal == 0:
    raise ValueError("❌ FAISS index is empty! No data found.")

print(f"✅ FAISS index loaded successfully! Total vectors: {vector_db.index.ntotal}")


# 🔍 INPUT
query = input("Nhập câu hỏi của bạn: ")

# 📌 Query FAISS to find document relatively
retrieved_docs = vector_db.similarity_search(query, k=5)
retrieved_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

print("Retrieved text:", retrieved_text)

# 🧠 Format prompt cho LLaMA 3.1
prompt = f"""
You are an AI assistant that answers questions based on retrieved context.

Context:
{retrieved_text}

Question:
{query}

Answer:
"""

# 💡 Send promt to LLaMA 3.1
response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])


# 📌 Answer
print("\n📌 Answer:", response["message"]["content"])