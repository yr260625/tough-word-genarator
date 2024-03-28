from fastapi import FastAPI
from app.tough_word import ToughWord
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "https://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/tough-word")
def generate_tough_word():
    tough_word = ToughWord()
    return {"result": tough_word.generate()}
