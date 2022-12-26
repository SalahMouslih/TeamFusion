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
                                    'email varchar (50),'
                                    'phone varchar (30),'
                                    'skills varchar (150) NOT NULL,'
                                    'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                    )
    
    cur.execute('DROP TABLE IF EXISTS projects;')
    cur.execute('CREATE TABLE projects (id serial PRIMARY KEY,'
                                    'name varchar (20)  NOT NULL unique,'
                                    'description text,'
                                    'skills varchar (150) NOT NULL,'
                                    'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                    )
    sql = "INSERT INTO resumes (name,email,phone,skills) VALUES ('dummy name', 'email@email,com', '111111','SQL, Linux, Git')"
    cur.execute(sql)
    sql_ = "INSERT INTO projects (name,description,skills) VALUES ('Project_1','We are looking for a developer with strong skills in Python, Java, and SQL. Experience with Linux and Git is a plus','Python, Java, SQL, Linux, Git')"
    cur.execute(sql_)
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

def insert_proj(project:dict):
    conn = psycopg2.connect(
        host=POSTGRES_SERVER,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD)
    cur = conn.cursor()
    sql = "INSERT INTO projects (name,description,skills) VALUES (%(name)s, %(description)s,%(skills)s)"
    cur.execute(sql,project)
    conn.commit()
    cur.close()
    conn.close()

def list_proj():
    conn = psycopg2.connect(
        host=POSTGRES_SERVER,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM projects;")
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result

def sel_proj(name):
    conn = psycopg2.connect(
        host=POSTGRES_SERVER,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM projects WHERE name ='%s';" %name)
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result