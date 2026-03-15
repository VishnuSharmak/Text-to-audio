from flask import Flask, render_template, request, jsonify, send_file
import os, time
import pyttsx3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(STATIC_DIR, exist_ok=True)

app = Flask(__name__)

last_audio_file = None   # 🔥 STORE LAST AUDIO

def find_voice(engine, choice):
    for v in engine.getProperty("voices"):
        name = v.name.lower()
        lang = str(v.languages).lower()

        if choice == "female" and "female" in name:
            return v.id
        if choice == "male" and "male" in name:
            return v.id
        if choice == "hindi" and ("hindi" in name or "hi" in lang):
            return v.id
        if choice == "indian" and ("india" in name or "en" in lang):
            return v.id

    return engine.getProperty("voices")[0].id

@app.route("/convert", methods=["POST"])
def convert():
    global last_audio_file

    text = request.form.get("text", "").strip()
    voice_choice = request.form.get("voice", "indian")

    if not text:
        return jsonify({"error": "Empty text"}), 400

    filename = f"audio_{int(time.time()*1000)}.mp3"
    audio_path = os.path.join(STATIC_DIR, filename)

    engine = pyttsx3.init()
    engine.setProperty("rate", 155)
    engine.setProperty("voice", find_voice(engine, voice_choice))

    engine.save_to_file(text, audio_path)
    engine.runAndWait()

    last_audio_file = filename  # ✅ SAVE FILE NAME

    return jsonify({
        "success": True,
        "audio_url": f"/static/{filename}"
    })

# 🔥 FIXED DOWNLOAD ROUTE
@app.route("/download-audio")
def download_audio():
    if not last_audio_file:
        return "No audio generated yet", 404

    return send_file(
        os.path.join(STATIC_DIR, last_audio_file),
        as_attachment=True
    )

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
