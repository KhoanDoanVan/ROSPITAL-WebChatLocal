from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
  return render_template( 'index.html')

@app.route('/message')
def message():
  return jsonify({"message": "Hello, World!"})

@app.route('/data', methods=['POST'])
def receive_data():
  data = request.json
  print("Received:", data)
  return jsonify({"message": "Data received successfully"})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=2000)