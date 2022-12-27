# Authors:

- Salah Eddine
- Imad
- Boubakar



# Description:

The idea of this project is to match consultants to projects based on their skills.

for this, we parse Resume skills as well as project keywords and then perform the matching.

we used **FastAPI** for developing the backend

More on FastAPI : [Here](https://fastapi.tiangolo.com/).

## Getting started

First, create a virtual environement and install the requirements:

```
python3 -m venv env
```

```
source ./env/bin/activate
```

```
pip install -r requirements.txt
```
## Endpoints

## Launch the application

To launch the application, run:

```
uvicorn app.core.main:app --reload
```

uvicorn is an ASGI (async server gateway interface) compatible web server. It's (simplified) the binding element that handles the web connections from the browser or api client and then allows FastAPI to serve the actual request.

The server is running in development mode on your local machine (localhost or 127.0.0.1). You can a request by opening your browser and entering `http://127.0.0.1:8000` in the url.

