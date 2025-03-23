import qrcode
import os
import socket

def get_wifi_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print("⚠️ Can't get IP WiFi:", e)
        return "127.0.0.1"

ip_address = get_wifi_ip()
port = "2100"
urlString = f"http://{ip_address}:{port}"

qr_filename = "server_qr.png"

if os.path.exists(qr_filename):
    os.remove(qr_filename)

qr = qrcode.make(urlString)
qr.save(qr_filename)

print(f"✅ QR code : {urlString}")