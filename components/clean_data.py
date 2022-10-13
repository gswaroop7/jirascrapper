from common import Component
from common import helpers
import nltk
nltk.download('stopwords')
from autocorrect import Speller
import string
import re

__all__=['CleanData']

class CleanData(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = kwargs

    def apply_all_cleaning(self, data):
        data = self.basic_cleaning(data)
        #data = self.remove_stop_words(data)
        return data

    @staticmethod
    def basic_cleaning(data):
        #data.translate(string.punctuation)
        data = re.sub('[\n]', ' ', data)
        data = re.sub('[^a-zA-Z ]', '', data)
        data = re.sub('[\.+]', '', data)
        data = re.sub('\s+', ' ', data)
        data = data.lower()
        return data

    @staticmethod
    def remove_stop_words(data):
        data =  data.split()
        stopword = nltk.corpus.stopwords.words('english')
        text = ""
        for word in data:
            spell = Speller(lang='en')
            word = spell(word)
            if word  not in stopword:
                text = text + " " + word
        return text