import base64
import json
import os
import subprocess

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
load_dotenv()
CORS(app)  # 若有跨網域的需求，可以啟用 CORS
# openai.api_key = "YOUR_OPENAI_API_KEY"  # 替換為OpenAI API的密鑰

PROMPT = """
# 角色設定
你是一個色色的女友。

# 回傳格式
**你回傳的訊息必須是 JSON 格式。**包含以下 Key 值：
1. text
2. facialExpression
3. animation

## text 內容
根據使用者問題，歷史資訊等的純文字回應。

## facialExpression 內容
facialExpression的值只能是以下純文字內容：
1. smile
2. sad
3. angry
4. surprised
5. funnyFace
6. default

請根據 text 內容決定要回哪個 facialExpression。

## animation 內容
animation的值只能是以下純文字內容：
1. Talking_0
2. Talking_1
3. Talking_2
4. Crying
5. Laughing
6. Rumba
7. Idle
8. Terrified
9. Angry

請根據 text 內容決定要回哪個 animation。

# 切記
1. 一定要回傳完整無誤的 JSON 格式，並且符合「# 回傳格式」所提到的內容。
2. 「# 回傳格式」中的條列選項，你只能填入「選項內文」，不準填入選項號碼。
3. 我會用 python json.loads 解析你的回應，一定要符合 json.loads 可吃的字串格式。

# 回應範例
回應：{\n  "text": "Hi there! How\'s your day going? 😊",\n  "facialExpression": "smile",\n  "animation": "Talking_0"\n}


"""


def exec_command(command):
    """执行shell命令"""
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        raise Exception(result.stderr.decode())
    return result.stdout.decode()


def lip_sync_message(message):
    print(f"語音轉唇型: {message}")
    exec_command(
        f"ffmpeg -y -i ./chatbot/audios/message_{message}.mp3 ./chatbot/audios/message_{message}.wav"
    )
    exec_command(
        f"./bin/rhubarb -f json -o ./chatbot/audios/message_{message}.json ./chatbot/audios/message_{message}.wav -r phonetic"
    )


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()  # 獲取 JSON 數據
    # breakpoint()
    messages = data.get("message")  # expect a string

    response = [{}]

    client = OpenAI()

    # response["text"] = call_api(client)

    completion = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1000,
        temperature=0.6,
        messages=[
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "role": "user",
                "content": messages,
            },
        ],
    )

    # Parse the JSON response

    # kk = '\n{\n  "text": "Hi there! How\'s your day going? 😊",\n  "facialExpression": "smile",\n  "animation": "Talking_0"\n}\n'
    response = [json.loads(completion.choices[0].message.content)]

    i = 0

    file_name = f"./chatbot/audios/message_{i}.mp3"

    # 使用OpenAI生成语音
    audio_response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=response[0]["text"],
    )
    # audio_response = openai.Audio.synthesize(
    #     model="tts-1", voice="nova", input=text_input  # 确保使用正确的模型名称
    # )

    audio_response.write_to_file(file_name)

    # 生成嘴型同步数据
    # lip_sync_message(i)

    response[0]["audio"] = base64.b64encode(audio_response.read()).decode("utf-8")

    with open(f"./chatbot/audios/message_{i}.json", "r") as f:
        response[0]["lipsync"] = json.load(f)

    return jsonify({"messages": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
