## Authors:

- Salah Eddine
- Imad
- Boubakar

## Description:

TeamComp is an API that utilizes data to match consultants to projects based on their skills.

for this, we parse Resume skills as well as project keywords and then perform the matching.

The API was developed using **FastAPI** and was hosted using Gitlab pipelines to a AWS free tier **EC2** instance.
The API is normally up and running at [http://23.23.33.169:80](http://23.23.33.169:80). Yes! an IP address! because every fancy website URL hides an ip address behind! 

Unfortunately, due to some CPU utilization problems *- a common problem when using free services -* , the API is inaccessible most of the time :disappointed:.

But here is a better idea :bulb: : clone the project locally so you can explore the codebase and even reuse some bits in your projects! (Just make sure to inculde an attribution :smiley: )

More on FastAPI : [Here](https://fastapi.tiangolo.com/).

More on Gitlab Pipelines : [Here](https://docs.gitlab.com/ee/ci/pipelines/). 

## Run the app locally

*To run the app locally, you should have [Docker](https://docs.docker.com/get-docker/) installed on your machine.*

First, clone the project to a local directory using :

```
git clone https://gitlab.com/ensae-dev/projects_2022_2023/data-solution.git
```
Then tap this command to access the root directory.
```
cd data-solution
```

Finally, run the following command to create a docker image and initiate some beautiful containers.

```
docker-compose up -d
```

This might take a while, so you might go grab some coffee.

## Launch the application

The server now is running in development mode on your local machine (localhost or 127.0.0.1). Open your browser and tap `http://127.0.0.1:8000` to access the API.

## Endpoints

You can check the documentation at http://127.0.0.1:8000/docs.

## Final note

Feel free to share with us any question, remark or feedback!
