import pytest
import json
from fastapi.testclient import TestClient
from requests_toolbelt.multipart.encoder import MultipartEncoder
from app.core.main import app 

@pytest.fixture 
def client():
    with TestClient(app) as client:
        yield client



def test_upload(client):

    '''
    filename = "files/resume_01.pdf"
    
    file = MultipartEncoder(
        fields={'file': ('filename', open(filename, 'rb'), 'application/pdf')}
        )

    response = client.post("/uploadresume",
                           data=file,
                           headers={"Content-Type": "multipart/form-data"}
                           )

    assert response.status_code == 200
    files = {'file': ("resume_01.pdf", open(test_file, 'rb'))}
    response = client.post('/app/core/main/uploadresume', files=files)
    print(test_file)
    print(response.json())
        '''
    test_file = "files/resume_01.pdf"

    with test_file.open('rb') as f:
        files = {'files': f}
        response = client.post('/uploadresume',
                            files=files)
    assert 0
    #assert response.status_code == 303
    #assert response.json() == {"message": True} or response.json() == {"message": False}



'''
def test_prediction_json(client):
    res = client.post('/uploadresume',
                      json={'text': "When Sebastian Thrun started working on self-driving cars \
                          at Google in 2007, few people outside of the company took him seriously. \
                              I can tell you very senior CEOs of major American car companies would \
                                  shake my hand and turn away because I wasn’t worth talking to, said \
                                      Thrun, in an interview with Recode earlier this week.)"}) 
                                      # Send a POST request on the route /spacy/prediction
    data = json.loads(res.data) # Convert binary result res.data to Dict

    expected_result = {
        '2007': 'DATE',
        'American': 'NORP',
        'Recode': 'ORG',
        'Sebastian Thrun': 'PERSON',
        'earlier this week': 'DATE',
    }

    assert data == expected_result
'''git