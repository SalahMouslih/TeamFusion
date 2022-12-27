from pydantic import BaseModel, BaseSettings, Field


class DBCreds(BaseSettings):
    db_uri: str = Field(..., env="DB_URI")

    class Config:
        env_file = '.env'


class Input(BaseModel):
    sentence: str


class Resume(BaseModel):
    name: str
    email: str
    phone: str
    degree: str
    skills: list
    tot_exp: int


class Resumes(BaseModel):
    Resumes: list
