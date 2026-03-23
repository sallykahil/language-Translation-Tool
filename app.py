#“I implemented the translation tool using an external API.
#  Due to Azure tenant access issues, I used an alternative API to complete the functionality.”
from flask import Flask, request, jsonify, render_template
import requests

from deep_translator import GoogleTranslator
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json()

        text = data.get("text")
        source = data.get("source")
        target = data.get("target")

        translated = GoogleTranslator(source=source, target=target).translate(text)

        return jsonify({"translated": translated})

    except Exception as e:
        return jsonify({"error": str(e)}) 
if __name__ == "__main__":
    app.run(debug=True)