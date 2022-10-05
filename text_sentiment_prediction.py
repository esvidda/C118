import pandas as pd
import numpy as np

import tensorflow
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from datetime import datetime

# datos de entrenamiento
train_data = pd.read_csv("./static/data_files/tweet_emotions.csv")    
training_sentences = []

for i in range(len(train_data)):
    sentence = train_data.loc[i, "content"]
    training_sentences.append(sentence)

# cargar modelo
model = load_model("./static/model_files/Tweet_Emotion.h5")

vocab_size = 40000
max_length = 100
trunc_type = "post"
padding_type = "post"
oov_tok = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)

# asignar emoticones para diferentes emociones
emo_code_url = {
    "empty": [0, "./static/emoticons/Empty.png"],
    "sadness": [1,"./static/emoticons/Sadness.png" ],
    "enthusiasm": [2, "./static/emoticons/Enthusiasm.png"],
    "neutral": [3, "./static/emoticons/Neutral.png"],
    "worry": [4, "./static/emoticons/Worry.png"],
    "surprise": [5, "./static/emoticons/Surprise.png"],
    "love": [6, "./static/emoticons/Love.png"],
    "fun": [7, "./static/emoticons/fun.png"],
    "hate": [8, "./static/emoticons/hate.png"],
    "happiness": [9, "./static/emoticons/happiness.png"],
    "boredom": [10, "./static/emoticons/boredom.png"],
    "relief": [11, "./static/emoticons/relief.png"],
    "anger": [12, "./static/emoticons/anger.png"]
    
    }
# escribir la función para predecir la emoción
def predict(text):
    predicted_emotion=""
    predicted_emotion_img_url=""

    if text!="":
        sentence=[]
        sentence.append(text)

        sequences = tokenizer.texts_to_sequences(sentence)

        padded = pad_sequences(
            sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type
        )
        testing_padded = np.array(padded)
        
        predicted_class_label = np.argmax(model.predict(testing_padded), axis=1)
        print(predicted_class_label)

        for key, value in emo_code_url.items():
            if value[0] == predicted_class_label:
                predicted_emotion_img_url = value[1]
                predicted_emotion = key
        return predicted_emotion,predicted_emotion_img_url

def show_entry():
    day_entry_list = pd.read_csv("./static/assets/data_files/data_entry.csv")

    day_entry_list = day_entry_list.iloc[::-1]

    date1 = (day_entry_list['date'].values[0])
    date2 =(day_entry_list['date'].values[1])
    date3= (day_entry_list['date'].values[2])

    entry1 = (day_entry_list['text'].values[0])
    entry2 =(day_entry_list['text'].values[1])
    entry3= (day_entry_list['text'].values[2])

    emotion1 = (day_entry_list['emotion'].values[0])
    emotion2 =(day_entry_list['emotion'].values[1])
    emotion3= (day_entry_list['emotion'].values[2])

    emotion_url1=""
    emotion_url2=""
    emotion_url3=""

    for key, value in emo_code_url.items():
        if key==emotion1:
            emotion_url1=value[1]
        if key==emotion2:
            emotion_url2=value[1]
        if key==emotion3:
            emotion_url3=value[1]

    return [
        {
            "date": date1,
            "entry": entry1,
            "emotion": emotion1,
            "emotion_url": emotion_url1
        },
        {
            "date": date2,
            "entry": entry2,
            "emotion": emotion2,
            "emotion_url": emotion_url2
        },
        {
            "date": date3,
            "entry": entry3,
            "emotion": emotion3,
            "emotion_url": emotion_url3
        }
    ]