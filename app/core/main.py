from fastapi import FastAPI
import spacy 
import json
from pydantic import BaseModel
from typing import List
from pyresparser import ResumeParser
from fastapi import FastAPI, File, UploadFile, Form
from nltk.tokenize import word_tokenize
from typing import Optional

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


@app.get("/hello/{name}")
async def root(name:str):
    return {"noms": name}


@app.post("/upload/")
def upload(file: UploadFile = File(...)):
    try:
        file_location = f"files/{file.filename}"

        contents =  ResumeParser(file_location).get_extracted_data()
        print(contents)
        return  {"message": file_location}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()


@app.post('/extract')
def exctract(text : str):
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
