import ollama

# Khởi tạo mô hình
model = "llama3.1"

# Bắt đầu chat
while True:
    user_input = input("Bạn: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Tạm biệt!")
        break
    
    response = ollama.chat(model=model, messages=[{"role": "user", "content": user_input}])
    print("AI:", response['message']['content'])