import pytest
import json
from fastapi.testclient import TestClient
from requests_toolbelt.multipart.encoder import MultipartEncoder
from app.core.main import app 
from app.core import database 


@pytest.fixture 
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def test_db():
    db = database.init_db()
    yield db


def test_home(client):
    
    response = client.get('/home')

    assert response.status_code == 200
    assert response.headers["Content-Type"] == 'text/html; charset=utf-8'



def test_upload(client,test_db):

    filename = "files/resume_01.pdf"
    response = client.post("/uploadresumes",
                            files ={"file": ("filename", open(filename, "rb"), "application/json")}
                        )
    #resume = client.session.get("resume")
    assert response.status_code == 303
    assert response.is_redirect == True


def test_list_resumes(client,test_db):
    
    expected_resume = [
        {
        'email': 'email@email,com',
        'name': 'dummy name',
        'phone': '111111',
        'skills': 'SQL, Linux, Git'
        }
    ]
    
    response = client.get("/resumes")
    
    assert response.context["resumes"] == expected_resume
    assert response.status_code == 200
    assert response.headers["Content-Type"] == 'text/html; charset=utf-8'


def test_upload_project(client,test_db):
    
    data={
        "name" : "dummy project",
        "text" : "dummy text"
    }
    response = client.post("/uploadprojects",
                            data = data
                        )
    assert response.status_code == 303


def test_list_proj(client,test_db):
    
    expected_output=[
        {
        "name" : "Project_1",
        "description" : "We are looking for a developer with strong skills in Python, Java, and SQL. Experience with Linux and Git is a plus",
        "skills" : 'Python, Java, SQL, Linux, Git'
        }
    ]

    response = client.get("/projects")

    assert response.context["projects"] == expected_output
    assert response.status_code == 200
    assert response.headers["Content-Type"] == 'text/html; charset=utf-8'


def test_match(client, test_db):
    response = client.get('/match')

    assert response.context["projects"] == [{'name': 'Project_1'}] 
    assert response.status_code == 200
    assert response.headers["Content-Type"] == 'text/html; charset=utf-8'


def test_match_teams(client,test_db):
    data={
        "name" : "Project_1",
        "number" : 1
    }
    response = client.post("/matchs",
                            data = data
                        )

    assert response.context['teams'] == [{'name': 'dummy name', 'num_skills': 3, 'proj_name': 'Project_1'}]
    assert response.status_code == 200
    assert response.headers["Content-Type"] == 'text/html; charset=utf-8'

    