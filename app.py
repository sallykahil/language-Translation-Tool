"""
Language Translation Tool (app1).

This version uses `deep_translator.GoogleTranslator`.
It may require internet access depending on how the library connects.
"""

from flask import Flask, request, jsonify, render_template
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

        if source == target:
            return jsonify({"translated": text})

        translated = GoogleTranslator(source=source, target=target).translate(text)

        return jsonify({"translated": translated})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)