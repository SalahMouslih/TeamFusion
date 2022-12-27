from app.models import model
import psycopg2
from urllib.parse import urlparse

db_creds = model.DBCreds()

def init_db():
    parsed_db_uri = urlparse(db_creds.db_uri)
    conn = psycopg2.connect(
        host=parsed_db_uri.hostname,
        database=parsed_db_uri.path[1:],
        user=parsed_db_uri.username,
        password=parsed_db_uri.password)
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
      host=db_creds.db_host,
        database=db_creds.db_database,
        user=db_creds.db_username,
        password=db_creds.db_password.get_secret_value())
    cur = conn.cursor()
    sql = "INSERT INTO resumes (name,email,phone,skills) VALUES (%(name)s, %(email)s, %(phone)s,%(skills)s)"
    cur.execute(sql,resume)
    conn.commit()
    cur.close()
    conn.close()

def list():
    conn = psycopg2.connect(
        host=db_creds.db_host,
        database=db_creds.db_database,
        user=db_creds.db_username,
        password=db_creds.db_password.get_secret_value())
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM resumes;")
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result

def insert_proj(project:dict):
    conn = psycopg2.connect(
        host=db_creds.db_host,
        database=db_creds.db_database,
        user=db_creds.db_username,
        password=db_creds.db_password.get_secret_value())
    cur = conn.cursor()
    sql = "INSERT INTO projects (name,description,skills) VALUES (%(name)s, %(description)s,%(skills)s)"
    cur.execute(sql,project)
    conn.commit()
    cur.close()
    conn.close()

def list_proj():
    parsed_db_uri = urlparse(db_creds.db_uri)
    conn = psycopg2.connect(
        host=parsed_db_uri.hostname,
        database=parsed_db_uri.path[1:],
        user=parsed_db_uri.username,
        password=parsed_db_uri.password)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM projects;")
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result

def sel_proj(name):
    parsed_db_uri = urlparse(db_creds.db_uri)
    conn = psycopg2.connect(
        host=parsed_db_uri.hostname,
        database=parsed_db_uri.path[1:],
        user=parsed_db_uri.username,
        password=parsed_db_uri.password)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM projects WHERE name ='%s';" %name)
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result