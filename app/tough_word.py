import pickle
import markovify

class ToughWord():
    def __init__(self):
        pass

    def generate(self):
        with open("static/tough_word_model.pkl", "rb") as f:
            tough_word_model = pickle.load(f)
            sentence = tough_word_model.make_sentence() or ""
            return sentence.replace(" ", "")

