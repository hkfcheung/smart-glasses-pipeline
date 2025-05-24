from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ingest", methods=["POST"])
def ingest_data():
    data = request.get_json()
    print("Received data:", data)

    # Store, forward, or process it here
    return jsonify({"status": "success", "received": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
