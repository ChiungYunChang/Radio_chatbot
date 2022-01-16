
from scipy import spatial
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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

# score = [0.156, 0.003, 0.002, 0.009, 0.286, 0.127, 0.012, 0.011, 0.032, 0.023, 0.012, 0.004, 0.005, 0.058, 0.024, 0.014, 0.003, 0.031, 0.004, 0.012, 0.502, 0.01, 0.047, 0.017, 0.009, 0.012, 0.007, 0.051]
# print(np.shape([score]*2215))
# calcu_simi(score)