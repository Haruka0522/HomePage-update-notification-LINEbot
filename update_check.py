import os
from requests_html import HTMLSession
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 環境変数
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]


def PushMessage():
    Authorization = "Bearer {"+LINE_CHANNEL_ACCESS_TOKEN+"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': Authorization,
    }
    data = '{\n    "messages":[\n        {\n            "type":"text",\n            "text":"Update the homepage https://sasayama-jh.sasayama.jp/"\n        }\n    ]\n}'
    response = requests.post(
        'https://api.line.me/v2/bot/message/broadcast', headers=headers, data=data)
    return response


session = HTMLSession()
r = session.get("https://sasayama-jh.sasayama.jp/")
latest_article = r.html.find("article")[0].text

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credential = {
    "type": "service_account",
    "project_id": os.environ['SHEET_PROJECT_ID'],
    "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
    "private_key": os.environ['SHEET_PRIVATE_KEY'],
    "client_email": os.environ['SHEET_CLIENT_EMAIL'],
    "client_id": os.environ['SHEET_CLIENT_ID'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
}
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credential, scope)
gc = gspread.authorize(credentials)
wks = gc.open("past_article").sheet1
past_article = str(wks.acell("A1").value)
wks.update_acell("A1", latest_article)
if latest_article != past_article:
    PushMessage()
