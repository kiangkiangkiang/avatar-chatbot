import base64
import json
import subprocess
from typing import Callable

from chatbot.utils.logger import logger


def read_image(file: str) -> str:
    with open(file, "rb") as image_file:
        result = base64.b64encode(image_file.read()).decode("utf-8")
    return result


def exec_command(command):
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        raise Exception(result.stderr.decode())
    return result.stdout.decode()


def lip_sync_message(mp3_file_name):
    logger.info(f"語音轉唇型: {mp3_file_name}")
    exec_command(f"ffmpeg -y -i {mp3_file_name}.mp3 {mp3_file_name}.wav")
    exec_command(
        f"./bin/rhubarb -f json -o {mp3_file_name}.json {mp3_file_name}.wav -r phonetic"
    )


def get_lip(
    use_rhubarb=False, mp3_file_name: str = None, write_file_func: Callable = None
):
    if use_rhubarb and mp3_file_name is not None and write_file_func is not None:
        # 生成嘴形同步數據
        write_file_func(f"{mp3_file_name}.mp3")
        lip_sync_message(mp3_file_name)

        with open(f"{mp3_file_name}.json", "r") as f:
            result = json.load(f)
        return result

    else:
        with open(f"./chatbot/audios/default.json", "r") as f:
            result = json.load(f)
        return result
