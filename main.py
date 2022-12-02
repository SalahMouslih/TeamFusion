from fastapi import FastAPI
import spacy 
import json

model = spacy.load('en_core_web_sm')

app = FastAPI()


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
