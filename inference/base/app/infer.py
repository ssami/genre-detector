from fastapi import FastAPI
from pydantic import BaseModel
from app.lib.tools import preprocess, postprocess
from model import LoadedModel
import json

app = FastAPI()
LABEL_PREFIX = '__label__'
model = LoadedModel()


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
