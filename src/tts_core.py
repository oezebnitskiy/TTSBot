# tts_core

# What?: From text -> to .mp3

from gtts import gTTS
from bs4 import BeautifulSoup

import ffmpeg
import requests

folder_id = "b1gi27tinsla0p6a0a3p"
iam_token = "t1.9euelZrKl8zKipWXz5TOkZ6blpiVl-3rnpWals2Sz5zLi5uRiovPz8nHmsfl9PcwXG50-e8_G2C_3fT3cApsdPnvPxtgvw.fCD6WSBxsPOA38gr53PJGk9KwzveUhYU9gSLzwH1D_mBVfeTn-lVm-xmLcDvj60xqqc0wJR9VqavRB5LjIYBAg"

def synthesize(lang, text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': text,
        'lang': lang,
        'speed': "1.7",
        'folderId': folder_id
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


def extract_text(text):
    for word in text.replace("\n", " ").split(" "):
        if "https://" in word:
            url = word
            break
        if "http://" in word:
            url = word
            break
    print(f"Loaded file: {url}")
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    text = ""
    for i in soup.find_all('p'):
        text += i.text.strip()
    return text

def detect_lang(text):
    ru = 0
    en = 0
    for sym in text:
        sym = sym.lower()
        if sym in "йцукенгшщзфывапролдячсмитьбюхъэёю":
            ru += 1
        elif sym in "qwertyuiopasdfghjklzxcvbnm":
            en += 1
    if ru > en:
        return "ru-RU"
    else:
        return "en-US"

def fromText2Mp3(filename, lang, text):
    # Create speech file

    with open(filename, "wb") as f:
            for audio_content in synthesize(lang, text):
                f.write(audio_content)

    # Increase speed via ffmpeg
    """
    stream = ffmpeg.input(filename)
    audio = stream.audio.filter("atempo", 1.5)
    ret_filename = filename.replace(".mp3","x2.mp3")
    out = ffmpeg.output(audio, ret_filename)
    out.run(overwrite_output=True)
    """
    return filename



