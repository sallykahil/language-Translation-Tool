"""
Offline Language Translation Tool (Argos Translate).
 
"""

from flask import Flask, request, jsonify, render_template

import argostranslate.translate as argos_translate

app = Flask(__name__)

LANGS = {"en", "ar", "fr"}
PIVOTS = ["en", "ar", "fr"]


def offline_translate(text: str, source: str, target: str) -> str:
    """
    Translate offline using Argos Translate.

    If the direct model (source -> target) isn't installed, try a pivot:
    source -> pivot -> target.
    """
    try:
        return argos_translate.translate(text, source, target)
    except Exception:
        last_err = None
        for pivot in PIVOTS:
            if pivot == source or pivot == target:
                continue
            try:
                mid = argos_translate.translate(text, source, pivot)
                return argos_translate.translate(mid, pivot, target)
            except Exception as e:
                last_err = e
        raise last_err


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or {}
    text = data.get("text")
    source = data.get("source")
    target = data.get("target")

    try:
        if not isinstance(text, str) or not text.strip():
            return jsonify({"error": "Text must be a non-empty string."}), 400

        # Offline mode can't auto-detect without extra tooling/models.
        if source == "auto":
            return jsonify({"error": "Offline mode requires selecting From as en/ar/fr (no Auto-detect)."}), 400

        if source not in LANGS or target not in LANGS:
            return jsonify({"error": "Unsupported language. Use en/ar/fr only."}), 400

        if source == target:
            return jsonify({"translated": text})

        translated = offline_translate(text, source, target)
        return jsonify({"translated": translated})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

