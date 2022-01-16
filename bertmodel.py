import torch
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import torch.nn as nn
import transformers
# from googlesearch import search
import requests
from sklearn.metrics.pairwise import cosine_similarity
from youtube_search import YoutubeSearch


def calcu_simi(score,top):
    dataa = pd.read_csv('DATASET.csv', usecols=['admiration','amusement','anger','annoyance','approval','caring','confusion','curiosity','desire','disappointment','disapproval','disgust','embarrassment','excitement','fear','gratitude','grief','joy','love','nervousness','optimism','pride','realization','relief','remorse','sadness','surprise','neutral'])
    singer = pd.read_csv('DATASET.csv', usecols=['Artist','Title'])
    dataa = dataa.to_numpy()
    singer = singer.to_numpy()
    shape = np.shape(dataa)[0]
    score = [score] * shape
    simi = cosine_similarity(score,dataa)
    idx = np.argsort(simi[0])[::-1]
    return singer[idx[:top]]



class GoEmotionDataset():
    def __init__(self, texts, targets):
        self.texts = texts
        self.targets = targets
        self.tokenizer = transformers.SqueezeBertTokenizer.from_pretrained(
            "squeezebert/squeezebert-uncased", do_lower_case=True
        )
        self.max_len = 35

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        target = self.targets[index]
        text = self.texts[index]

        inputs = self.tokenizer.encode_plus(text,
                           None,
                           add_special_tokens=True,
                           max_length=self.max_len,
                           padding="max_length",
                           truncation=True)

        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]

        return {
            "ids": torch.tensor(ids, dtype=torch.long),
            "mask": torch.tensor(mask, dtype=torch.long),
            "targets": torch.tensor(self.targets[index], dtype=torch.long),
        }


class EmotionClassifier(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.bert = transformers.SqueezeBertModel.from_pretrained("squeezebert/squeezebert-uncased")
        self.bert_drop = nn.Dropout(0.3)
        self.out = nn.Linear(768, num_classes)
        # print(self.out)
        self.step_scheduler_after = "batch"


    def forward(self, ids, mask):
        o_2 = self.bert(ids, attention_mask=mask)["pooler_output"]
        b_o = self.bert_drop(o_2)
        output = self.out(b_o)
        return output




_CLASS_NAMES = [
    "admiration",
    "amusement",
    "anger",
    "annoyance",
    "approval",
    "caring",
    "confusion",
    "curiosity",
    "desire",
    "disappointment",
    "disapproval",
    "disgust",
    "embarrassment",
    "excitement",
    "fear",
    "gratitude",
    "grief",
    "joy",
    "love",
    "nervousness",
    "optimism",
    "pride",
    "realization",
    "relief",
    "remorse",
    "sadness",
    "surprise",
    "neutral",
]

mapping = dict(zip(range(len(_CLASS_NAMES)),_CLASS_NAMES))



tokenizer = transformers.SqueezeBertTokenizer.from_pretrained(
            "squeezebert/squeezebert-uncased", do_lower_case=True
        )

def score_sentence(text, topn=28):
    max_len = 35
    model = EmotionClassifier(num_classes=28)
    ckpg = torch.load('model.bin', map_location='cpu')
    model.load_state_dict(ckpg['state_dict'])
    model.eval()

    with torch.no_grad():

        inputs = tokenizer.encode_plus(text,
        None,
        add_special_tokens=True,
        max_length=max_len,
        padding="max_length",
        truncation=True)
        ids = inputs["input_ids"]
        ids = torch.LongTensor(ids).unsqueeze(0)

        attention_mask = inputs["attention_mask"]
        attention_mask = torch.LongTensor(attention_mask).unsqueeze(0)

        output = model.forward(ids, attention_mask)[0]
        output = torch.sigmoid(output)
        # print(output)
        # probas, indices = torch.sort(output)

    # probas = probas.cpu().numpy()[::-1]
    # indices = indices.cpu().numpy()[::-1]
    listvalue = []
    for i in range(len(output)):
        # print(mapping[i], round(output[i].item(),3))
        listvalue.append(round(output[i].item(),3))
    # print(listvalue)
    top_emo = np.argsort(listvalue)[::-1]
    top = 6
    songs = calcu_simi(listvalue, top)
    res = get_google_search(songs)
    link = pie_chart(listvalue,_CLASS_NAMES)
    return res, link
    # for i, p in zip(indices[:topn], probas[:topn]):
    #     print(mapping[i], p)

def get_google_search(text):
    link_text = []
    for i in range(len(text)):
        sen = f"{text[i][0]} {text[i][1]}"
        # print(sen)
        # links = search(sen, stop=1)#stop=5代表取得前5個結果
        links = YoutubeSearch(sen, max_results=1).to_dict()[0]['url_suffix']
        link = f"https://www.youtube.com{links}"
        # print(link)
        link_text.append([sen,link])
    return link_text

def pie_chart(confi,emotion):
    idx = np.argsort(confi)[::-1][:5]
    confi = np.array(confi)[idx]
    emotion = np.array(emotion)[idx]
    # print("emotion",emotion)
    # print(confi,emotion)
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lavender']
    # matplotlib套件顏色列表
    explode = (0.1, 0, 0, 0, 0)  # 切一塊出來距離0.1
    import matplotlib.pyplot as plt
    plt.pie(confi, explode=explode, labels=emotion, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('pie_con.png')
    plt.close()
    link = glucose_graph()
    return link
    # plt.show()

import pyimgur

def glucose_graph():
    CLIENT_ID = "7963c995e3e0c9c"
    PATH = "pie_con.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    return uploaded_image.link

# print(score_sentence("i'm so excited"))

# print(score_sentence("i'm feeling very confident about this situation"))
# res = f"{score[0][0]} {score[0][1]}"
# print(res)
