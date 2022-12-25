from fastapi import FastAPI, Request, status
import spacy 
import json
from pydantic import BaseModel
from typing import List
from pyresparser import ResumeParser
from fastapi import FastAPI, File, UploadFile, Form
from nltk.tokenize import word_tokenize
from typing import Optional
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from io import  BytesIO
from resume_parser import resumeparse
from tempfile import TemporaryDirectory
import os
import aiofiles
from app.core import database
from starlette.datastructures import URL


database.init_db()



model = spacy.load('en_core_web_sm')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



class Input(BaseModel):
    sentence: str

class Resume(BaseModel):
    name : str
    email : str
    phone : str
    degree : str
    skills : List
    tot_exp : int



@app.get("/")
async def root():
    return RedirectResponse(url='/home')


@app.get("/home", response_class = HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/uploadresume",response_class=HTMLResponse )
async def form_post(request: Request, msg: Optional[str] = None,):
    return templates.TemplateResponse("add_resume.html", {"request": request, "msg": msg})

@app.post("/uploadresumes")
def upload(request:Request, file: UploadFile = File(...)):
    try:
        skills = []
        f = open('files/skills.txt', 'r')
        skills = f.read().split('\n')

        #create temp directory
        with TemporaryDirectory() as tmp_dir:              
            file_path = os.path.join(tmp_dir,'resume.pdf')
            #write file to temp_dir
            with open(file_path, "wb") as f:
                f.write(file.file.read())
                
                #extract resume infos
                #data = ResumeParser(file_path).get_extracted_data()
                data = resumeparse.read_file(file_path)
                

                resume = {}
                resume["name"] = data["name"]
                resume["email"] = data["email"]
                resume["phone"] = data["phone"]
                resume["degree"] = data["degree"]
                resume["skills"] = []
                resume["skills"] = [skill for skill in data["skills"] if skill.lower() in skills]
                print(resume["skills"])    
                resume["tot_exp"] = data["total_exp"]
                database.insert(resume)
                
                message = True
                redirect_url = URL(request.url_for('form_post')).include_query_params(msg=message)
                return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


    except Exception:
            message = False
            redirect_url = URL(request.url_for('form_post')).include_query_params(msg=message)
            return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)


    finally:
        file.file.close()




@app.get("/resumes")
async def list(request:Request):
    res = database.list()
    resumes = []
    for data in res:
        resume = {}
        resume["name"] = data[1]
        resume["email"] = data[2]
        resume["phone"] = data[3]
        resume["skills"] = data[4]
        resumes.append(resume)

    return templates.TemplateResponse("list_resumes.html", {"request": request, "resumes": resumes})


@app.get('/extract/{text}')
def exctract(text : str):
    #db.insert(text)
    entities : Dict = {}
    doc = model(text)
    for entity in doc.ents:
        entities[entity.text] = entity.label_
    return json.dumps(entities)

'''
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
'''