import subprocess

# Chạy file load_model.py trước để tạo FAISS database
print("🚀 Đang xử lý tài liệu và tạo FAISS database...")
subprocess.run(["python3", "load_model.py"], check=True)

# Chạy file query_response.py để nhập câu hỏi và lấy phản hồi
print("🔍 Đang khởi động hệ thống truy vấn...")
subprocess.run(["python3", "query_response.py"], check=True)

print("✅ Quá trình hoàn tất!")