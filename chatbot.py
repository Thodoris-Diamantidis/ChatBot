import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

import requests
import api_token

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

def clean_up_sentene(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentene(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i,word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_token.api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data


def get_response(intents_list, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag']  == tag:
            result = random.choice(i['responses'])
            if tag == "weather":
                print("Please enter a city:")
                city = input()
                # Call the OpenWeatherMap API to get the weather data for the city
                data = get_weather(city)

                # Get the weather description and temperature from the API response
                description = data['weather'][0]['description']
                temperature = data['main']['temp']

                # Choose a random response from the intents.json file and replace placeholders with actual values
                response = random.choice(i['responses'])
                response = response.format(city=city, description=description, temperature=temperature)
                result = response
                break
            break
    return result

print("GO! Bot is running!")

while True:
    message = input()
    ints = predict_class(message)
    res = get_response(ints, intents)
    print(res)