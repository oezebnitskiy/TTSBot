import argparse
import requests

folder_id = "b1gi27tinsla0p6a0a3p"
iam_token = "t1.9euelZqQiZaJyJLGnYyXzM3IiZSNnO3rnpWals2Sz5zLi5uRiovPz8nHmsfl9PcpHwV1-e8eUEmc3fT3aU0CdfnvHlBJnA.id62ii_0rkhg7A8qFwNficrHwBkTF9XzDU3Oqs6Bo6YFkKByMqfemZ4GmndzvhfBNlk24FGppEOG2uzq49AIAA"

def synthesize(folder_id, iam_token, text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': text,
        'lang': 'en-US',
        'folderId': folder_id
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk

with open("new_sample.ogg", "wb") as f:
        for audio_content in synthesize(folder_id, iam_token, "Poshel nhui pidorast ebat suka"):
            f.write(audio_content)