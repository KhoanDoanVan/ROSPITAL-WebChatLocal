from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from read_files import read_docs

# 🚀 Load documents
doc_files = ["quy_che_hoat_dong_benh_vien.docx", "danh_sach_bac_si.docx"]
documents = [read_docs(file) for file in doc_files]
corpus = "\n".join(documents)

# 🔥 Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# 📝 Seperate files to sub contexts
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_text(corpus)

# 🏛️ Create FAISS database
vector_db = FAISS.from_texts(chunks, embedding_model)

# ✅ Save FAISS database to file
vector_db.save_local("faiss_index")