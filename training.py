import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?','!','.',',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern) # returns list of words
        words.extend(word_list)
        documents.append((word_list, intent['tag'])) # this is so we know that this word_list belongs to the category intent['tag']
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words)) # remove duplicates

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb')) 
#Saves words to file name words.pkl in binary mode. 'wb' flah indicates that the file is being opened for writing in binary mode
#The pickle.dump function serializes the words object and writes it to the file
#By saving these variables to disk, i can load them later without having to re-run the code to generate them.This is useful if you have a large dataset that takes a long time to process or if you want to share the variables with others wwho dont have access to the original data
pickle.dump(words, open('classes.pkl', 'wb'))

#I am doing this because these are not numerical values and to use them in a neural network i need numerical values
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

"""
The code starts by defining an empty list called training and a list of zeros called output_empty,
 which has the same length as the classes list.
Then, for each document in documents, it creates a bag of words for that document by setting the value
of each word in the words list to either 1 or 0 depending on whether or not it appears in the word_patterns list
(which is just the list of words in the document after lemmatization and lowercasing).
The output_row variable is also created by setting the value at the index of the correct class in classes to 1
and leaving all other values as 0.
Finally, the training list is populated with the bag of words and corresponding output row for each document.
"""
