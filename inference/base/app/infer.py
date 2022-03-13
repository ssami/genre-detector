import json

from app.lib.tools import preprocess, postprocess
from app.model import LoadedModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
LABEL_PREFIX = '__label__'
model = LoadedModel()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


class TextInfer(BaseModel):
    text: str


@app.get("/")
def hello():
    return "hello"


@app.post("/predict")
def predict(req: TextInfer):
    text = preprocess(req.text)
    results = model.predict(text, k=1)
    label_conf = postprocess(results, LABEL_PREFIX)
    return json.dumps(label_conf)


@app.get("/info")
def get_info():
    return model.info
