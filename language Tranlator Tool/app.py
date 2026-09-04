'''resquest: data from the browser sends to our server
jsonify: convert python dictionary into a proper JSON HTTP response
requests: to make HTTP requests to the translation API
'''
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

#read the translation API URL from environment variables
TRANSLATE_API_URL = os.getenv("TRANSLATE_API_URL") 


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()

    text = data.get("text", "").strip()
    source = data.get("source", "en")
    target = data.get("target", "en")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if source == "auto":
        source = "en"  # MyMemory's free endpoint doesn't support true auto-detect

    params = {
        "q": text,
        "langpair": f"{source}|{target}"
    }

    try:
        response = requests.get(TRANSLATE_API_URL, params=params, timeout=10)
        response.raise_for_status() #checks the HTTP status code
        result = response.json() #parse the JSON response

        if result.get("responseStatus") != 200:
            error_detail = result.get("responseDetails", "Translation failed")
            return jsonify({"error": error_detail}), 502

        translated_text = result["responseData"]["translatedText"]
        return jsonify({"translatedText": translated_text})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Could not reach translation service: {str(e)}"}), 503


if __name__ == "__main__":
    app.run(debug=True)