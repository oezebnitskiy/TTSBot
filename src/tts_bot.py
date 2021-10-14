# tts_bot 

# What?: bot -> get text -> return .mp3

import telebot
import time
import requests
import datetime

import tts_core


bot_token = '1272682265:AAFAdMZj_zbNeXhzkRcaZwSzTABzSV1Wgio'
VOICE_LEN = 5000
bot = telebot.TeleBot(bot_token)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(message.json)
    # Handling links
    if ("https://" in message.text) or ("http://" in message.text):
        text = tts_core.extract_text(message.text)
    else:
        text = message.text
    filename = f"../data/text-{str(datetime.datetime.now().timestamp()).split('.')[1]}.mp3"
    speech = filename
    print(f"Catched: {filename}")
    ret_filename = tts_core.fromText2Mp3(speech, tts_core.detect_lang(text), text)
    # Send speech file
    print(f"Sending: {filename}")
    audio = open(ret_filename, 'rb')
    bot.send_voice(message.chat.id, audio, reply_to_message_id=message.message_id)


@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    # Если zip -> unzip 
    # Если mobi, pdf, fb2 -> в  fulltext
    # Если txt -> озвучивать
    # Получить текст
    print(message.json)
    # requests
    file_info = bot.get_file(message.document.file_id)
    time.sleep(10)
    text = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_token, file_info.file_path)).text
    # Разобрать его в обратном порядке по N-символов (n=7500*4)
    text_batches = [text[i*VOICE_LEN:(i+1)*VOICE_LEN] for i in range(len(text)//VOICE_LEN+1)]
    # Каждый блок: озвучить -> отправить
    count = 0
    for text in text_batches:
        count += 1
        print(f"Sending: {count}/{len(text_batches)}")
        filename = f"../data/text-{str(datetime.datetime.now().timestamp()).split('.')[1]}.ogg"
        ret_file = tts_core.fromText2Mp3(filename, tts_core.detect_lang(text), text)
        print(f"Created: {filename}")
        audio = open(ret_file, 'rb')
        time.sleep(2)
        bot.send_voice(message.chat.id, audio)
        print(f"Sent: {filename}")
    bot.send_message(message.chat.id, f"Finished {message.document.file_name}")



if __name__ == '__main__':
    bot.infinity_polling()