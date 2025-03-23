from flask import Flask, request, jsonify, render_template
import subprocess
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import ollama


app = Flask(__name__, template_folder='templates')


# 🔥 Load embedding model và FAISS khi server khởi động
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
faiss_path = os.path.abspath("train/build/faiss_index")


try:
    print(f"📌 Loading FAISS index from: {faiss_path}")
    vector_db = FAISS.load_local(faiss_path, embeddings=embedding_model, allow_dangerous_deserialization=True)
    
    if vector_db.index.ntotal == 0:
        raise ValueError("❌ FAISS index is empty! No data found.")

    print(f"✅ FAISS index loaded successfully! Total vectors: {vector_db.index.ntotal}")
except Exception as e:
    print(f"❌ Error loading FAISS: {e}")
    vector_db = None



# Route: Default
@app.route('/')
def home():
  return render_template( 'index.html')

# Route: Message
@app.route('/message')
def message():
  return jsonify({"message": "I'm an assistant of you to answer questions about Hospital 🏥"})

# Route: Data
@app.route('/data', methods=['POST'])
def receive_data():
  data = request.json
  print("Received:", data)
  return jsonify({"message": "Data received successfully"})

# Route: Query AI
@app.route('/query', methods=['POST'])
def query_ai():
    if vector_db is None:
        return jsonify({"error": "FAISS index is not loaded!"}), 500
   

    data = request.json
    query = data.get("question", "").strip()

    if not query:
        return jsonify({"error": "No question provided!"}), 400

    # Retrieve top 5 documents
    retrieved_docs = vector_db.similarity_search(query, k=3)
    retrieved_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

    print("retrieved_text:", retrieved_text)

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
    return jsonify({"answer": response["message"]["content"]})

if __name__ == '__main__':

  try:
      print("Loading model and saving to vector DB...")
      subprocess.run(["python3", "train/build/load_model.py"], check=True)
      print("Model loaded successfully ✅")
  except subprocess.CalledProcessError as e:
      print("Error loading model ❌:", e)

  app.run(host='0.0.0.0', port=2100)