from fastapi import FastAPI, Request, status
from fastapi import File, UploadFile, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.datastructures import URL

import os
import json
from tempfile import TemporaryDirectory
from typing import List, Optional

import spacy 
from nltk.tokenize import word_tokenize
from resume_parser import resumeparse

from app.models import model
from app.core import database

description = """
TeamComp API guides you into builiding optimal teams. 

## Resumes

You will be able to:

* **Add resumes** by parsing extracted skills .
* **Read resumes**.

## Projects

You will be able to:

* **Add projects** required skills.
* **Read projects**.

## Teams

With this, you can **build teams** for your projects by matching skills 
"""



tags_metadata = [
    {
        "name": "home",
        "description": "Home page with _goto_ access.",
    }
    ,
    {
        "name": "resume",
        "description": "Parse skills from member resumes by using  **ResumeParser** open source library.",
        "externalDocs": {
            "description": "More about ResumeParser",
            "url": "https://pypi.org/project/resume-parser/ ",
        },
    },
    {
        "name": "resumes",
        "description": "List Resumes by fetching the database.",
       
    },
    {
        "name": "project",
        "description": "Parse skills from project descripitions by using  **Spacy**, the famous entities extraction library.",
        "externalDocs": {
            "description": "More about Spacy",
            "url": "https://spacy.io/usage/ ",
        },
       
    },
    {
        "name": "projects",
        "description": "List Projects with their respective required skills.",
       
    },
    {
        "name": "match",
        "description": "Matches projects and resumes on skills.",
       
    },
]

nlp = spacy.load("en_core_web_sm")
database.init_db()

templates = Jinja2Templates(directory="templates")


app = FastAPI(
    title="TeamComp",
    description=description,
    version="0.0.1",
    contact=[{

        "name": "Salah-Eddine EL MOUSLIH",
        "email": "salah-eddine.elmouslih@ensase.frr",
    },
    {
        "name": "Imad BOUDROUA",
        "email": "iboudroua@ensae.fr",
    },
    {
        "name": "Boubakar SIDEBE",
        "email": "bsidebe@ensae.fr"
    }
    ],
    openapi_tags=tags_metadata
)




@app.get("/")
async def root(tags=["home"]):
    return RedirectResponse(url='/home')


@app.get("/home", response_class = HTMLResponse, tags=["home"])
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/uploadresume",response_class=HTMLResponse , tags=["resume"])
async def upload_res(request: Request, msg: Optional[str] = None,):
    return templates.TemplateResponse("add_resume.html", {"request": request, "msg": msg})

@app.post("/uploadresumes",response_model = model.Resumes, tags=["resume"])
def upload_resume(request:Request, file: UploadFile = File(...)):
    try:
        #load skills file
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
                resume["tot_exp"] = data["total_exp"]
                
                #save infos
                database.insert(resume)
                
                #redirect with success message
                message = True

                redirect_url = URL(request.url_for('upload_res')).include_query_params(msg=message)
                response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
                
                return response

    except Exception:
                        
            #redirect with failure message
            message = False
            redirect_url = URL(request.url_for('upload_res')).include_query_params(msg=message)
            return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

    finally:
        file.file.close()

@app.get("/resumes", response_model = model.Resumes , tags=["resumes"])
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


@app.get("/uploadproject",response_class=HTMLResponse, tags=["project"])
async def upload_proj(request: Request, msg: Optional[str] = None,):
    return templates.TemplateResponse("add_project.html", {"request": request, "msg": msg})


@app.post("/uploadprojects", tags=["project"])
async def upload_project(request:Request, name: str = Form(...), text: str = Form(...)):  
    try: 
        #pass text to model
        doc = nlp(text)
        entities = [ent.text for ent in doc.ents if ent.label_ == "IT"]
                
        project = {}
        project["name"] = name
        project["description"] = text
        #extract project skills
        project["skills"] = [doc.text.lower() for doc in doc.ents]        
        
        #save project to database
        database.insert_proj(project)

        #redirect with succes message
        message = True
        redirect_url = URL(request.url_for('upload_proj')).include_query_params(msg=message)
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        return response

    except Exception:

        #redirect with failure message
        message = False
        redirect_url = URL(request.url_for('upload_proj')).include_query_params(msg=message)
        response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        return response


@app.get("/projects", response_model = model.Projects, tags=["projects"])
async def list_projects(request:Request):
    try:
        res = database.list_proj()
        projects = []
        for data in res:
            project = {}
            project["name"] = data[1]
            project["description"] = data[2]
            project["skills"] = data[3]
            projects.append(project)

        return templates.TemplateResponse("list_projects.html", {"request": request, "projects": projects})
    
    except Exception:
        message = False
        return templates.TemplateResponse("list_projects.html", {"request": request, "message": message})

@app.get("/match",tags=["match"])
async def match(request:Request):
    try:
        res = database.list_proj()
        projects = []
        for data in res:
            project = {}
            project["name"] = data[1]
            projects.append(project)
        
        return templates.TemplateResponse("match.html", {"request": request, "projects": projects})
    
    except Exception:
        message = False
        return templates.TemplateResponse("match.html", {"request": request, "message": message})

@app.post("/matchs", response_model = model.Teams, tags=["match"])
async def gen_teams(request:Request, name: str = Form(...), number: int  = Form(...)):

    try: 
        #retrieve project by passing project name
        project = database.sel_proj(name)
        
        # Get the required skills for the project
        required_skills = project[3]

        #retrieve resumes
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
            #add team member to teams list
            team.append(team_member)
        
        #sort team by number of required skills desc
        team = sorted(team, key=lambda x: x["num_skills"], reverse= True)

        #pass number of specified team members
        return templates.TemplateResponse("teams.html", {"request": request, "teams": team[:number]})
    
    except Exception:
        
        message = False
        return templates.TemplateResponse("teams.html", {"request": request, "message": message})
