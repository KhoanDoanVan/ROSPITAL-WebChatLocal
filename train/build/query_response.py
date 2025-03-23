import ollama
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

# 🔥 Load lại FAISS database
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")




# Sử dụng đường dẫn tuyệt đối
faiss_path = os.path.abspath("faiss_index")

# ✅ Debug: Kiểm tra xem thư mục FAISS có tồn tại không
if not os.path.exists(faiss_path):
    raise FileNotFoundError(f"❌ FAISS index not found at {faiss_path}")

# Load FAISS với quyền đọc an toàn
print(f"📌 Loading FAISS index from: {faiss_path}")
vector_db = FAISS.load_local(faiss_path, embeddings=embedding_model, allow_dangerous_deserialization=True)

# ✅ Debug: Kiểm tra số lượng tài liệu trong FAISS
if hasattr(vector_db, "index") and vector_db.index.ntotal == 0:
    raise ValueError("❌ FAISS index is empty! No data found.")

print(f"✅ FAISS index loaded successfully! Total vectors: {vector_db.index.ntotal}")




# 🔍 Nhập câu hỏi từ người dùng
query = input("Nhập câu hỏi của bạn: ")

# 📌 Truy vấn FAISS để lấy tài liệu liên quan
retrieved_docs = vector_db.similarity_search(query, k=5)  # Lấy 5 đoạn phù hợp nhất
retrieved_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

# 🧠 Format prompt cho LLaMA 3.1
prompt = f"""
You are an AI assistant that answers questions based on retrieved context.

Context:
{retrieved_text}

Question:
{query}

Answer:
"""

# 💡 Gửi prompt đến LLaMA 3.1
response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])


# 📌 Hiển thị kết quả
print("\n📌 Answer:", response["message"]["content"])