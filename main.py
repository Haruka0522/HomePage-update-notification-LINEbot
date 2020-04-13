from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage,\
    ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, \
    PostbackTemplateAction, MessageTemplateAction, URITemplateAction
    )
import os
from requests_html import HTMLSession
import os

app = Flask(__name__)

#環境変数
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
session = HTMLSession()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "HP":
        r = session.get("https://sasayama-jh.sasayama.jp/")
        reply = r.html.find("article")[0].text
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)

