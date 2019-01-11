from flask import Flask
from flask import request
import re
import requests
import json
import os

app = Flask(__name__)


telegram_api_key = os.environ['telegram_bot_api']

def setLMGTFY(string, index):
    substring = string[index:]

    match = re.search('[!,.?]', substring)

    if match is not None:
        new_string = substring[:substring.find(match.group())]
    else:
        new_string = substring

    LMGTFY = 'https://lmgtfy.com/?q=' + ('+').join(new_string.split(' '))

    return LMGTFY;

@app.route('/', methods=['GET'])
def hello():
    return 'Hello World'

@app.route('/api', methods=['POST'])
def vis_webhook():
    incoming_json = request.get_json()


    TELEGRAM_URL = 'https://api.telegram.org/' + telegram_api_key +'/sendMessage'

    payload = {
        "chat_id": "407352782",
        "text": "None",
        "parse_mode": "HTML"
    }

    chat_id = incoming_json["message"]["chat"]["id"]
    chat_message = incoming_json["message"]["text"]

    pattern = re.compile(r"\bhow\b")

    for m in pattern.finditer(chat_message):
        if type(m.start()) == int:
            isHowQuestion = m.start()
            payload["text"] = setLMGTFY(chat_message, isHowQuestion)
            payload["chat_id"] = chat_id
            requests.post(TELEGRAM_URL, payload)
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
            break
        else:
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run()
