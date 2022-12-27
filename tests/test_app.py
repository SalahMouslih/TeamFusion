import pytest
import json
from fastapi.testclient import TestClient
from app.core.main import app 

@pytest.fixture 
def client():
    with TestClient(app) as client:
        yield client



def test_upload(client):

    filename = "files/resume_01.pdf"
    response = client.post("/uploadresumes",
                            files ={"file": ("filename", open(filename, "rb"), "application/json")}
                        )
    
    excpected_result ={
    "resume": {
        "name": "John Smith",
        "email": "email@email.com",
        "phone": "3868683442",
        "degree": [],
        "skills": [
            "SQL",
            "Java",
            "Apache Spark",
            "Python"
        ],
        "tot_exp": 0
    }
    }
    assert response.status_code == 303
    #assert response.json["resumes"] == excpected_result
    assert response.is_redirect == True

'''
def test_get_resume(client, test_upload):
    data = {'title': 'Hot Boat', 'description': 'This is a boat'}
    resp = client.post('/uploadresumes', params={"msg": "None"})
    response = test_upload
    assert response.text() == 0

'''
