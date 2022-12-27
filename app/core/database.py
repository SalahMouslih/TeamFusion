from os import getenv
import psycopg2


POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
POSTGRES_SERVER='127.0.0.1'
POSTGRES_DB='fastapi_db'

def init_db():
    conn = psycopg2.connect(
        host=POSTGRES_SERVER,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS resumes;')
    cur.execute('CREATE TABLE resumes (id serial PRIMARY KEY,'
                                    'name varchar (30) NOT NULL,'
                                    'email varchar (20),'
                                    'phone varchar (20),'
                                    'skills varchar (150) NOT NULL,'
                                    'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                    )
    
    sql = "INSERT INTO resumes (name,email,phone,skills) VALUES ('dummy name', 'email@email,com', '111111','None')"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def insert(resume:dict):
    conn = psycopg2.connect(
        host=POSTGRES_SERVER,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD)
    cur = conn.cursor()
    sql = "INSERT INTO resumes (name,email,phone,skills) VALUES (%(name)s, %(email)s, %(phone)s,%(skills)s)"
    cur.execute(sql,resume)
    conn.commit()
    cur.close()
    conn.close()

def list():
    conn = psycopg2.connect(
        host=POSTGRES_SERVER,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM resumes;")
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result
