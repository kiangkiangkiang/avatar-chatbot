import base64
import json

from dotenv import load_dotenv

load_dotenv()
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from chatbot.session import UserData, sessions
from chatbot.utils.config import DEBUG, HOST, PORT, USE_LIP_TOOL
from chatbot.utils.logger import logger
from chatbot.utils.openai_tools import openai_tools
from chatbot.utils.prompt_store import PromptStore
from chatbot.utils.toy_tools import get_lip, read_image

app = Flask(__name__)
app.secret_key = "dev"
CORS(app)


@app.route("/on_page_create", methods=["POST"])
def on_page_create():
    data = request.get_json()
    if data["pageId"] not in sessions:
        sessions[data["pageId"]] = UserData()
    return jsonify(success=True), 200


@app.route("/on_page_remove", methods=["POST"])
def on_page_remove():
    data = request.get_json()
    if data["pageId"] in sessions:
        sessions.pop(data["pageId"])
    return jsonify(success=True), 200


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    messages = data.get("message")
    user_id = data.get("pageId")

    system_prompt = PromptStore.default_prompt()

    if user_id not in sessions:
        logger.warning(f"User ID: {user_id} not in memory. It should not happen.")
        sessions[user_id] = UserData()

    if len(sessions[user_id].chat_memory) == 0:
        sessions[user_id].append_memory(role="system", content=system_prompt)

    sessions[user_id].append_memory(role="user", content=messages)

    # Debug
    # if True:
    #     clean_response = openai_tools.dummy_response
    #     response = [clean_response]
    #     with open("./chatbot/audios/default.mp3", "rb") as f:
    #         response[0]["audio"] = base64.b64encode(f.read()).decode("utf-8")

    #     response[0]["lipsync"] = get_lip(
    #         use_rhubarb=False,
    #     )

    #     base64_image = read_image("./chatbot/img/sample.png")

    #     return jsonify({"messages": response, "image_data": base64_image})

    clean_response = openai_tools.create_chat_completions_with_func_try(
        unstable_func=json.loads,
        messages=sessions[user_id].chat_memory,
        user_id=user_id,
    )

    response = [clean_response]

    audio_response = openai_tools.text_to_speech(input_text=response[0]["text"])

    response[0]["audio"] = base64.b64encode(audio_response.read()).decode("utf-8")
    response[0]["lipsync"] = get_lip(
        use_rhubarb=USE_LIP_TOOL,
        mp3_file_name=f"./chatbot/audios/tmp/tmp_{str(uuid.uuid4())}",
        write_file_func=audio_response.write_to_file,
    )

    return jsonify({"messages": response})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
