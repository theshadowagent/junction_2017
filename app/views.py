from collections import defaultdict
import the_model
from ml.Classifier_ml import text_to_emojis


emojies_mapping = {
    'dynamic': '5',
    'intellectual': '6',
    'sentimental': '2',
    'mystical': '4',
    'sad': '1',
    'funny': '0',
    'teen': '3',
    'inspiring': '7'
}

coefs = {
    'dynamic': 1,
    'intellectual': 1.2,
    'sentimental': 0.9,
    'mystical': 1,
    'sad': 0.7,
    'funny': 1,
    'teen': 0.65,
    'inspiring': 1,
}


class Movie:

    def __init__(self, index, data):
        self.index = index
        self.title = None
        self.relevant_percent = 0.5
        self.reviews = None
        self.emojis = []
        self.data = data
        self._emojis_counter = defaultdict(int)

    def calc_proc(self, freq):
        sum = 0
        for key, value in freq:
            sum += value
        res = [(key, round(value / sum * 100, 1)) for key, value in freq]
        return res

    def filter_freq(self, freq):
        norm_em = self.normalize_coefs(freq)
        sorted_em = sorted(norm_em, key=lambda x: x[1], reverse=True)

        emoji = [key for key, value in sorted_em if value > 13]
        self.emojis = [emojies_mapping[key] for key in emoji]
        return emoji, sorted_em

    def normalize_coefs(self, freq):
        d = dict(freq)
        for key in d:
            d[key] *= coefs[key]
            d[key] = round(d[key], 1)
        return list(d.items())

    def calc_emojis(self):
        if self.reviews:
            # em_freq = the_model.text_to_emoji(self.reviews)
            em_freq = text_to_emojis(self.reviews)
            frq = self.calc_proc(em_freq)
            em, old = self.filter_freq(frq)
        else:
            self.emojis = []
            em, old = [], []

        print(self.title, old, em)
