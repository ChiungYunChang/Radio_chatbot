from flask import Flask, request, abort
from sklearn.metrics.pairwise import cosine_similarity
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,PostbackTemplateAction,URITemplateAction
# from linebot.models import *
import configparser
import json
import bertmodel
import numpy as np
import pyimgur
import re
import requests
app = Flask(__name__)
from youtube_search import YoutubeSearch
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))
handler = WebhookHandler(config.get('line-bot', 'channel-secret'))

to = "7624c3f4631e86e87d9165c93ce716c5"

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

def GetWeather(station):
    end_point = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=rdec-key-123-45678-011121314"
    # end_point ="https://opendata.epa.gov.tw/ws/Data/AQI/?$format=json"
    data = requests.get(end_point).json()
    data = data["records"]["location"]

    target_station = "not found"
    for item in data:
        if item["locationName"] == str(station):
            target_station = item
    return target_station


def MakeWeather(station):

    WeatherData = GetWeather(station)
    if WeatherData == "not found":
        return False

    WeatherData = WeatherData["weatherElement"]
    msg = "Weather - " + "台南"
    msg += "\nTemperature = " + WeatherData[3]["elementValue"] + "℃\n"
    msg += "Humidity = " + \
        str(float(WeatherData[4]["elementValue"]) * 100) + "% RH\n"

    song_rec = None
    if float(WeatherData[3]["elementValue"]) > 20.0:
        descript = "Hot summer sunny swimming water ice cream"
    elif float(WeatherData[4]["elementValue"]) * 100 > 50:
        descript = "Raining depression umbrella wet "
    else:
        descript = "getting cold freezing out snow "

    song, image_url = bertmodel.score_sentence(descript)
    i = np.random.randint(5)
    result = f"Here are some songs for you \n {song[i][0]} {song[i][1]}"

    return msg, result


def get_google_search(text):
    link_text = []
    # for i in range(len(text)):
    sen = f"{text[0]} {text[1]}"
    links = YoutubeSearch(sen, max_results=1).to_dict()[0]['url_suffix']
    link = f"https://www.youtube.com{links}"
    link_text.append([sen,link])
    return link_text

def air():
    r = requests.get("https://opendata.epa.gov.tw/ws/Data/AQI/?$format=json", verify=False)
    list_of_dicts = r.json()
    return list_of_dicts

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id=event.source.user_id
    text = event.message.text
    reply_all = []
    greetingn_text = re.compile('good night')
    greetingn_textn = re.compile('good morning')
    greetingn_textm = re.compile('morning')
    greetingn_textn1 = re.compile('night')
    we_textn1 = re.compile('weather')
    nextsong_text = re.compile('next song')
    help_text = re.compile("help")
    joke_text = re.compile("joke")

    # weather
    # if text == 'good morning' or text == 'good night'or text =='morning'or text=='night':
    if we_textn1.findall(text) or greetingn_text.findall(text) or greetingn_textn.findall(text) or greetingn_textn1.findall(text) or greetingn_textm.findall(text):
        message, song_rec = MakeWeather("安平")
        # message = "Hello !  Today is quite cold you'd better wear extra layers. "
        reply_all.append(TextSendMessage(text=message))
        reply_all.append(TextSendMessage(text=song_rec))

    elif help_text.findall(text) :
        message = "Tell me how you feel and fing the best song for you !  \nIf you enter the \"good morning\" or \"good night\" you will get the weather enter \"next song\" I wil find another song for you :)\nBTW, Do you want to hear joke ? Just enter \"joke\" ! "
        reply_all.append(TextSendMessage(text=message))

    elif joke_text.findall(text):
        joke = []
        joke.append("What type of music are balloons afraid of? \nPop music.")
        joke.append("Why did the fish make such a good musician? \nHe knew his scales.")
        joke.append("What is the most musical part of your body? \nYour nose because you can blow and pick it.")
        joke.append("What makes songs, but never sings? \nNotes.")
        joke.append("Why is a piano so hard to open? \nBecause the keys are on the inside.")
        joke.append("How do you make a bandstand?\nTake away their chairs.")
        joke.append("What is the difference between a fish and a piano? \nYou can’t tuna fish.")
        joke.append("What’s a cat’s favorite subject in school? \nMEWsic.")
        joke.append("How can you tell if a singer’s at your door? \nThey can’t find the key and don’t know when to come in.")
        joke.append("Why was music coming from the printer? \n The paper was jamming.")
        joke.append("Which one of Santa's helpers was the best singer? \nElf-is Presley!")
        joke.append("Why did the pianist keep banging his head against the keys? \n He was playing by ear!")
        joke.append("What do you get when you put a radio in the fridge? \nCool music!")
        joke.append("What do you call a cow that can play a musical instrument? \nA moo-sician!")
        joke.append("What makes music in your hair? \nA headband!")
        i = np.random.randint(14)
        reply_all.append(TextSendMessage(text=joke[i]))



    elif  nextsong_text.findall(text) :
        message =[]
        message.append(" Hope you enjoy it ! \n")
        song = pd.read_csv('DATASET.csv', usecols=['Artist', 'Title'])
        song = song.to_numpy()
        i = np.random.randint(2210)
        res = get_google_search(song[i])
        message.append(f"{res[0][0]} {res[0][1]}")
        res = f"{res[0][0]} {res[0][1]}"
        reply_all.append(TextSendMessage(text=res))

    else :
        song, image_url = bertmodel.score_sentence(text)
        i = np.random.randint(5)
        result = f"{song[i][0]} {song[i][1]}"
        # reply_all.append(TextSendMessage(text=result))

        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        reply_all.append(image_message)
        reply_all.append(TextSendMessage(text=result))
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=image_url))
    line_bot_api.reply_message(event.reply_token, reply_all)





if __name__ == "__main__":
    app.run(debug=True)