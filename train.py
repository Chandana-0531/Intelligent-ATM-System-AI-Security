
import pickle
import os

ENCODINGS_PATH = "encodings.pkl"

def load_encodings():
    if os.path.exists(ENCODINGS_PATH):
        with open(ENCODINGS_PATH, "rb") as f:
            return pickle.load(f)
    return {}

def save_encodings(enc):
    with open(ENCODINGS_PATH, "wb") as f:
        pickle.dump(enc, f)


