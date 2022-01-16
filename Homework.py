from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser
import json


def register(text, user_id):
    # text: 接收到的String
    # user_id: User的Line ID
    

    name = text[text.find(':')+1:text.find('/')]
    student_id = text[text.rfind(':')+1:]
    print(student_id)

    # 讀取註冊資料庫
    with open('./registered_data.json', 'r', encoding='utf-8') as file:
        registered_user = json.load(file) 

    # 檢查重複註冊
    if str(user_id) in registered_user:
        return '您已經註冊過囉！'

    
    # 新增使用者至註冊資料庫
    registered_user[user_id] = dict()
    registered_user[user_id]['Name'] = name
    registered_user[user_id]['Student_ID'] = student_id
    
    
    # 將註冊資料庫寫回檔案
    with open('./registered_data.json', 'w', encoding='utf-8') as file:
        json.dump(registered_user, file, ensure_ascii=False, indent=4)

    return '註冊成功！'
    
def HW1(user_id):
    # 讀取註冊資料庫
    with open('./registered_data.json', 'r', encoding='utf-8') as file:
        userDB = json.load(file)

        # 檢查重複註冊
    if str(user_id) in userDB:
        username = userDB[user_id]['Name']
        studentID = userDB[user_id]['Student_ID']
        info = 'Yor name is:' + username + " \n " + "Your student ID is:" + studentID
        # print(info)
        return info
    else:
        return '尚未註冊'

