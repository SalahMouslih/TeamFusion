from fastapi import FastAPI
import spacy 
import json
from pydantic import BaseModel
from typing import List



model = spacy.load('en_core_web_sm')

app = FastAPI()



class Input(BaseModel):
    sentence: str

class Extraction(BaseModel):
    first_index: int
    last_index: int
    name: str
    content: str

class Output(BaseModel):
    extractions: List[Extraction]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/spacy/prediction/{text}')
def prediction(text : str):
    #db.insert(text)
    entities : Dict = {}
    doc = model(text)
    for entity in doc.ents:
        entities[entity.text] = entity.label_
    return json.dumps(entities)


@app.post("/extractions", response_model=Output)
def extractions(input: Input):
    document = model(input.sentence)

    extractions = []
    for entity in document.ents:
      extraction = {}
      extraction["first_index"] = entity.start_char
      extraction["last_index"] = entity.end_char
      extraction["name"] = entity.label_
      extraction["content"] = entity.text
      extractions.append(extraction)

    return {"extractions": extractions}
