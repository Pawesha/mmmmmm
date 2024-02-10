from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()
        # Process the received data as needed
        return jsonify({"message": "POST request received successfully"})
    else:
        return "Home"

if __name__ == "__main__":
    app.run(debug=True)
