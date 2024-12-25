import base64
import json

from flask import Flask, jsonify, request
from flask_cors import CORS  # 引入 CORS

app = Flask(__name__)

CORS(app)  # 為整個應用啟用 CORS


from pathlib import Path

from openai import OpenAI

client = OpenAI()
speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!",
)
response.stream_to_file(speech_file_path)


def read_json_transcript(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def audio_file_to_base64(file):
    with open(file, "rb") as f:
        audio_bytes = f.read()
    return base64.b64encode(audio_bytes).decode("utf-8")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()  # 獲取 JSON 數據
    # breakpoint()
    user_message = data.get("message")  # 用 .get() 方法安全地獲取 'message'
    # breakpoint()
    messages = [
        {
            "text": "Hey dear... How was your day?",
            "audio": audio_file_to_base64("./chatbot/audios/intro_0.wav"),
            "lipsync": read_json_transcript("./chatbot/audios/intro_0.json"),
            "facialExpression": "smile",
            "animation": "Talking_1",
        },
        {
            "text": "I missed you so much... Please don't go for so long!",
            "audio": audio_file_to_base64("./chatbot/audios/intro_1.wav"),
            "lipsync": read_json_transcript("./chatbot/audios/intro_1.json"),
            "facialExpression": "sad",
            "animation": "Crying",
        },
    ]

    return jsonify({"messages": messages})

    if request.method == "GET":
        # 處理 GET 請求
        return jsonify({"message": "Hello from GET!"})

    if request.method == "POST":
        # 處理 POST 請求
        data = request.get_json()
        return jsonify({"message": "Hello from POST!", "received_data": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
