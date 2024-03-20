from fastapi import FastAPI
from app.tough_word import ToughWord

app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/tough-word")
def generate_tough_word():
    tough_word = ToughWord()
    return {"result": tough_word.generate()}
