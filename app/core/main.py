from fastapi import FastAPI
import spacy
import json
import nltk
nltk.download('punkt')
nltk.download('stopwords')

import rake_nltk
from rake_nltk import Rake
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

        contents = ResumeParser(file_location).get_extracted_data()
        print(contents)
        return {"message": file_location}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

@app.post("/text_extraction")
def skills_extractions(input: Input):
    r = Rake()
    res = []

    r.extract_keywords_from_text(input.sentence)
    print()

    for rating, keyword in r.get_ranked_phrases_with_scores():
        if rating > 4:
            res.append(keyword)

    return {"Key words": res}
