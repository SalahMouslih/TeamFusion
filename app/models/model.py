from pydantic import BaseModel


class Input(BaseModel):
    sentence: str

class Resume(BaseModel):
    name : str
    email : str
    phone : str
    degree : str
    skills : list
    tot_exp : int


class Resumes(BaseModel):
    Resumes : list
