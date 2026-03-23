# Language Translation Tool

This project is a small web app that translates text between:
- `en` (English)
- `ar` (Arabic)
- `fr` (French)

It includes **two Flask apps**:
- `app.py` = **App1** (Google-based translator via `deep_translator`)
- `app2.py` = **App2** (fully **offline** translator via **Argos Translate**)

## Project Files
- `app.py` : App1 (uses `deep_translator.GoogleTranslator`)
- `app2.py` : App2 (uses `argostranslate`)
- `download_models.py` : downloads offline Argos translation models (one-time)
- `templates/index.html` : UI (language dropdown + text + result)
- `static/style.css` and `static/script.js` : styling and frontend logic

## Setup (run once)
From the project folder:
```powershell
cd "C:\Users\dell\Desktop\SALLY\AI-Sally\language-Translation-Tool"
.\venv\Scripts\activate
pip install flask deep-translator argostranslate
```

## App1 (`app.py`) — GoogleTranslator (may need internet)
### Run
```powershell
python app.py
```
Open the URL Flask prints (usually `http://127.0.0.1:5000/`).

### How to use
- Choose `From` and `To`
- Type/paste text
- Click **Translate**

### Auto-detect
- The UI includes `Auto-detect`.
- App1 can generally accept `source="auto"` because `deep_translator` handles it.

## App2 (`app2.py`) — Fully Offline (no API keys)
App2 uses **Argos Translate** models that run locally on your machine.

### Step 1: Download models (internet ON for this step only)
```powershell
python download_models.py
```
After this finishes, you can turn off internet.

### Step 2: Run offline app
```powershell
python app2.py
```
Open the URL Flask prints.

### How to use
- Choose `From` as `en`, `ar`, or `fr`
- Choose `To` as `en`, `ar`, or `fr`
- Type/paste text
- Click **Translate**

### Important: Auto-detect is NOT supported in App2
- App2 expects `source` to be one of `en/ar/fr`.
- If you select `Auto-detect`, App2 returns an error.

## Difference Summary (App1 vs App2)
- **App1 (`app.py`)**: translation is handled by `deep_translator.GoogleTranslator` (internet may be required; no model download step).
- **App2 (`app2.py`)**: translation is handled by `argostranslate` using downloaded local models (internet not needed after `download_models.py`).

