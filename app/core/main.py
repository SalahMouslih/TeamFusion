from fastapi import FastAPI, Request, status
from fastapi import FastAPI, Depends, HTTPException
import spacy 
import json
from app.models import model
from typing import List
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
                #resume["skills"] = [skill for skill in data["skills"] if skill.lower() in skills]

                resume["skills"] = [s for s in skills if any(skill.lower() in s for skill in data["skills"])]

                print(resume["skills"])    
                resume["tot_exp"] = data["total_exp"]
                print(resume)
                #save infos
                database.insert(resume)
                
                message = True

                #redirect with success message
                redirect_url = URL(request.url_for('form_post')).include_query_params(msg=message)
                response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
                
                return response


    except Exception:
            message = False
            redirect_url = URL(request.url_for('form_post')).include_query_params(msg=message)
            return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    finally:
        file.file.close()

@app.get("/resumes")
async def list_resumes(request:Request):
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
    
    project = {}
    project["name"] = name
    project["description"] = text
    project["skills"] = [doc.text.lower() for doc in doc.ents]

    print(project)
    
    database.insert_proj(project)

    redirect_url = URL(request.url_for('form_post_proj')).include_query_params(msg=message)
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return response

@app.get("/projects")
async def list_proj(request:Request):
    res = database.list_proj()
    projects = []
    for data in res:
        project = {}
        project["name"] = data[1]
        project["description"] = data[2]
        project["skills"] = data[3]
        projects.append(project)

    return templates.TemplateResponse("list_projects.html", {"request": request, "projects": projects})

@app.get("/match")
async def match(request:Request):
    res = database.list_proj()
    projects = []
    for data in res:
        project = {}
        project["name"] = data[1]
        projects.append(project)
    
    return templates.TemplateResponse("match.html", {"request": request, "projects": projects})

@app.post("/matchs")
async def match_teams(request:Request, name: str = Form(...), number: int  = Form(...)):

    project = database.sel_proj(name)
    # Get the required skills for the project
    required_skills = project[3]

    res = database.list()
    
    resumes = []
    for data in res:
        resume = {}
        resume["name"] = data[1]
        resume["skills"] = data[4]
        resumes.append(resume)
    
    team = []
    # Iterate over the resumes
    for resume in resumes:
        team_member = {}
        team_member["proj_name"] = project[1]
        team_member["name"] = resume["name"]
        team_member["num_skills"] = 0
        # Get the skills of the resume
        skills = resume["skills"].split(",")
        
        # Check if the resume has the required skills
        for skill in skills:
            if (skill.lower() in required_skills) : team_member["num_skills"]+= 1
        team.append(team_member)
    
    team = sorted(team, key=lambda x: x["num_skills"], reverse= True)

    print(number)
    return templates.TemplateResponse("teams.html", {"request": request, "teams": team[:number]})