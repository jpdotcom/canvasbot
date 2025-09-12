from fastapi import FastAPI
import requests
from routers import users,assignments
from dotenv import load_dotenv 
import os 
load_dotenv()
CANVAS_BASE_URL = "https://canvas.case.edu/api/v1"
DATABASE_URL=os.getenv("DATABASE_URL")
TOKEN=os.getenv("TOKEN")
headers = {"Authorization": f"Bearer {TOKEN}"}

app=FastAPI()
app.include_router(users.router);
app.include_router(assignments.router)
@app.get("/")
def read_root():
    return {"message":"CanvasBot Backend Started Up!"}

def get_assignments(course_id):

    url = f"{CANVAS_BASE_URL}/courses/{course_id}/assignments"

    resp = requests.get(url,headers=headers);

    return resp.json()

def get_courses():

    url = f"{CANVAS_BASE_URL}/courses?enrollment_state=active"


    resp = requests.get(url,headers=headers)
    return resp.json()

@app.get("/testassignments/{course_id}")
def assignment(course_id):
    return get_assignments(course_id);

@app.get("/courses")

def courses():
    return get_courses();

@app.get("/assignments")

def getAllAssignments():

    courses = get_courses();
    assignments=[]
    for course in courses:

        assignments += get_assignments(course['id'])
    return assignments