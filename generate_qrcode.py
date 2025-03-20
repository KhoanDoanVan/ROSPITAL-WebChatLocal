import qrcode


ip_address = "192.168.31.245"
port = "2000"
urlString = f"http://{ip_address}:{port}"


qr = qrcode.make(urlString)

qr.save("server_qr.png")


print(f"QR code đã được tạo! Quét để truy cập: {urlString}")
