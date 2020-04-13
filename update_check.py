import os
from requests_html import HTMLSession
import requests

# 環境変数
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

def PushMessage():
    Authorization = "Bearer {"+LINE_CHANNEL_ACCESS_TOKEN+"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': Authorization,
    }
    data = '{\n    "messages":[\n        {\n            "type":"text",\n            "text":"Update the homepage https://sasayama-jh.sasayama.jp/"\n        }\n    ]\n}'
    response = requests.post('https://api.line.me/v2/bot/message/broadcast', headers=headers, data=data)
    return response

session = HTMLSession()

r = session.get("https://sasayama-jh.sasayama.jp/")

latest_article = r.html.find("article")[0].text

past_article = ""
try:
    with open("tmp/article_log.txt") as f:
        past_article = f.read()
except:
    with open("tmp/article_log.txt","w"):
        pass
with open("tmp/article_log.txt", mode="w") as f:
    f.write(latest_article)
if latest_article != past_article:
    PushMessage()
