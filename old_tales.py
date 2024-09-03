from flask import Flask, render_template, jsonify, request
import os
import time
from openai import OpenAI
from gtts import gTTS


# ChatGPT APIキー
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate-story", methods=["POST"])
def generate_story():
    prompt = request.json.get("prompt", "盛岡にまつわる昔話をしてください")

    # ChatGPTに物語を生成させる
    response = client.completions.create(engine="text-davinci-003", prompt=prompt, max_tokens=150)
    story = response.choices[0].text.strip()

    # 物語を音声に変換する
    tts = gTTS(text=story, lang="ja")
    filename = f"story_{int(time.time())}.mp3"
    filepath = os.path.join("static", filename)
    tts.save(filepath)

    return jsonify({"story": story, "audioUrl": filepath})


if __name__ == "__main__":
    app.run(debug=True)
