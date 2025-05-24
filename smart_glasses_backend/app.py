import os
import re
import warnings
from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import requests
from dotenv import load_dotenv
from urllib3.exceptions import NotOpenSSLWarning

# Suppress LibreSSL and insecure HTTPS warnings
warnings.simplefilter("ignore", NotOpenSSLWarning)
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter("ignore", InsecureRequestWarning)

# Load .env variables
load_dotenv()

app = Flask(__name__)

# Configuration
API_URL = os.getenv("API_URL", "https://api.llama.com/v1/chat/completions")
API_KEY = os.getenv("LLAMA_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "mySecurePass123")

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def ask_llama_for_cypher(payload_json: dict) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # New prompt that instructs LLaMA to return one clean query
    prompt = (
        "You are a Neo4j Cypher generation assistant.\n\n"
        "Given the following BLE payload, generate a syntactically valid Cypher query that can be executed in a single transaction using the Neo4j Python driver.\n\n"
        "- Use Cypher parameters like $device_id or $audio.raw_text (do not hardcode values).\n"
        "- Include WITH clauses where necessary (e.g., between CREATE and UNWIND).\n"
        "- Do NOT include multiple transactions or queries. Do NOT use semicolons.\n"
        "- Do NOT include markdown formatting or explanations. Just return the raw Cypher query.\n\n"
        f"BLE payload:\n{payload_json}"
    )

    payload = {
        "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
        "messages": [
            {"role": "system", "content": "You are a Neo4j graph assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        verify=False,
        timeout=180
    )

    print("Raw LLaMA response:", response.text)

    try:
        text = response.json().get("completion_message", {}).get("content", {}).get("text", "")
        # Extract Cypher code block
        cypher_blocks = re.findall(r"```cypher(.*?)```", text, re.DOTALL)
        if cypher_blocks:
            return cypher_blocks[0].strip()
        return text.strip()
    except Exception as e:
        print("Failed to parse Cypher from LLaMA:", e)
        return ""


@app.route("/ingest", methods=["POST"])
def ingest_data():
    data = request.get_json()
    print("Received BLE payload:", data)

    cypher = ask_llama_for_cypher(data)
    print("Generated Cypher:\n", cypher)

    if not cypher:
        return jsonify({"error": "LLaMA returned empty Cypher"}), 500

    try:
        with driver.session() as session:
            # Execute the generated Cypher query using parameters
            session.run(cypher, parameters=data)
    except Exception as e:
        print("Cypher execution failed:", e)
        return jsonify({"error": "Cypher failed", "details": str(e)}), 500

    return jsonify({
        "status": "success",
        "cypher": cypher
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
