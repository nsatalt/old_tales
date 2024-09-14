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
    # フロントエンドからのデータを取得（祖先情報と気分）
    ancestor = request.json.get("ancestor", "あなたの祖先")
    mood = request.json.get("mood", "普通")

    # 気分に基づいたプロンプトの変更
    if mood == "楽しい":
        prompt_mood = "楽しい"
    elif mood == "悲しい":
        prompt_mood = "少し悲しい"
    else:
        prompt_mood = "普通"

    # プロンプトの生成
    prompt = f"あなたは私のおばあちゃんです。８００字以内で盛岡の昭和初期の話を、実際にあった地名を加え、私の祖先の{ancestor}が登場する形で{prompt_mood}感じのお話をしてください。"

    # ChatGPTに物語を生成させる
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], max_tokens=800
    )
    story = response.choices[0].message.content.strip()

    # 物語を音声に変換する
    tts = gTTS(text=story, lang="ja")
    filename = f"story_{int(time.time())}.mp3"
    filepath = os.path.join("static", filename)
    tts.save(filepath)

    return jsonify({"story": story, "audioUrl": f"/static/{filename}"})


if __name__ == "__main__":
    app.run(debug=True)
