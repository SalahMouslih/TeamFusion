from pydantic import BaseModel, BaseSettings, Field, SecretStr


class DBCreds(BaseSettings):
    db_username: str = Field(..., env="POSTGRES_USER")
    db_password: SecretStr = Field(..., env="POSTGRES_PASSWORD")
    db_host: str = Field(..., env="POSTGRES_SERVER")
    db_database: str = Field(..., env="POSTGRES_DB")
    
    class Config:
        env_file = '.env'


class Input(BaseModel):
    sentence: str

class Resume(BaseModel):
    name : str
    email : str
    phone : str
    skills : list


class Resumes(BaseModel):
    Resumes : list


class Project(BaseModel):
    name : str
    description : str
    skills : list

class Projects(BaseModel):
    Projects : list

class Team(BaseModel):
    proj_name : str
    name : str
    num_skills : int

class Teams(BaseModel):
    Teams : list