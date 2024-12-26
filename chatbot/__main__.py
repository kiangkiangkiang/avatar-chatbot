import base64
import json

from dotenv import load_dotenv

load_dotenv()
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from chatbot.utils.config import DEBUG, HOST, PORT, USE_LIP_TOOL
from chatbot.utils.openai_tools import openai_tools
from chatbot.utils.prompt_store import PromptStore
from chatbot.utils.toy_tools import get_lip, read_image

app = Flask(__name__)


CORS(app)  # 若有跨網域的需求，可以啟用 CORS


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    messages = data.get("message")

    system_prompt = PromptStore.default_prompt()

    # Debug
    if True:
        clean_response = openai_tools.dummy_response
        response = [clean_response]
        with open("./chatbot/audios/default.mp3", "rb") as f:
            response[0]["audio"] = base64.b64encode(f.read()).decode("utf-8")

        response[0]["lipsync"] = get_lip(
            use_rhubarb=False,
        )

        base64_image = read_image("./chatbot/img/sample.png")

        return jsonify({"messages": response, "image_data": base64_image})

    clean_response = openai_tools.create_chat_completions_with_func_try(
        unstable_func=json.loads,
        user_msg=messages,
        system_prompt=system_prompt,
    )

    response = [clean_response]

    audio_response = openai_tools.text_to_speech(input_text=response[0]["text"])

    response[0]["audio"] = base64.b64encode(audio_response.read()).decode("utf-8")
    response[0]["lipsync"] = get_lip(
        use_rhubarb=USE_LIP_TOOL,
        mp3_file_name=f"./chatbot/audios/tmp_{str(uuid.uuid4())}",
        write_file_func=audio_response.write_to_file,
    )

    return jsonify({"messages": response})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
