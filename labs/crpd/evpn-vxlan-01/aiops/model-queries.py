# echo -e "cli\nshow configuration | display json\nexit\n" | docker exec -i clab-evpn-vxlan-01-leaf01 bash > leaf01_full_configuration.json
# curl -X POST -H "Content-Type: application/json" -d @leaf01_full_configuration.json http://localhost:5000/upload
# curl -X POST -H "Content-Type: application/json" -d '{"query": "How many routing instances are configured, and what are they? Please include there type."}' http://localhost:5000/query
# curl -X POST -H "Content-Type: application/json" -d '{"query": "Show me the status of the local interfaces for all of the EVPN instances on leaf01, and provide there attributes."}' http://localhost:5000/query

import json
import os

import dotenv
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)


def preprocess_json(json_data):
    text_data = ""
    for key, value in json_data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                text_data += f"{key}.{sub_key}: {json.dumps(sub_value)}\n"
        else:
            text_data += f"{key}: {json.dumps(value)}\n"
    return text_data


@app.route("/upload", methods=["POST"])
def upload_json():
    json_data = request.json
    preprocessed_data = preprocess_json(json_data)

    with open("network_data.txt", "w") as file:
        file.write(preprocessed_data)

    return jsonify({"message": "JSON data uploaded and preprocessed successfully."})


@app.route("/query", methods=["POST"])
def query_model():
    query_prompt = request.json["query"]

    with open("network_data.txt", "r") as file:
        network_data = file.read()

    prompt = f"{query_prompt}\n{network_data}"
    completion = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal:network-analysis:9fqy6KZX",
        messages=[{"role": "user", "content": prompt}],
    )

    return f"\n{completion.choices[0].message.content}\n"
    # return jsonify({"response": completion.choices[0].message.content})


# Set your OpenAI API key
dotenv.load_dotenv("../secrets.env")
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Create OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
