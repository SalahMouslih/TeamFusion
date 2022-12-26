from fastapi import FastAPI, Request, status
import spacy 
import json
from app.models import model
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
model = spacy.load("en_core_web_sm")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
                data = resumeparse.read_file(file_path)
                
                #parse resume infos
                resume = {}
                resume["name"] = data["name"]
                resume["email"] = data["email"]
                resume["phone"] = data["phone"]
                resume["degree"] = data["degree"]
                resume["skills"] = []
                resume["skills"] = [skill for skill in data["skills"] if skill.lower() in skills]
                print(resume["skills"])    
                resume["tot_exp"] = data["total_exp"]
                
                #save infos
                database.insert(resume)
                
                message = True
                
                #redirect with success message
                redirect_url = URL(request.url_for('form_post')).include_query_params(msg=message)
                response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
                #added post data to unit test
                response.form_data = resume
                return response


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


@app.get("/uploadproject",response_class=HTMLResponse )
async def form_post_proj(request: Request, msg: Optional[str] = None,):
    return templates.TemplateResponse("add_project.html", {"request": request, "msg": msg})


@app.post("/uploadprojects")
async def upload_project(request:Request, name: str = Form(...), text: str = Form(...)):
    
    
    print(name)
    print(text)
    doc = model(text)

    # Use spacy's named entity recognition to find IT-related entities
    entities = [ent.text for ent in doc.ents if ent.label_ == "IT"]
    message = True
    
    print(doc.ents)
    redirect_url = URL(request.url_for('form_post_proj')).include_query_params(msg=message)
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return response


