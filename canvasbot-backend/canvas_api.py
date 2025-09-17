import requests 
import crud;
from bs4 import BeautifulSoup
import schemas
CANVAS_BASE_URL = "https://canvas.case.edu/api/v1"
def get_header(token):

    
    return {"Authorization": f"Bearer {token}"}


def get_courses(token):

    url = f"{CANVAS_BASE_URL}/courses?enrollment_state=active"


    resp = requests.get(url,headers=get_header(token))
   
    return resp.json()


def get_course_by_id(course_id,token):
    
    url=f"{CANVAS_BASE_URL}/courses/{course_id}"

    resp = requests.get(url,headers=get_header(token))
    resp=resp.json()
    return resp['name']

def get_assignment(course_id,token):
    url = f"{CANVAS_BASE_URL}/courses/{course_id}/assignments"

    resp = requests.get(url,headers=get_header(token));

    return resp.json()

def sync_assignments(user_id,db):

    token=crud.get_user_token(db=db,user_id=user_id)
    all_courses = get_courses(token=token);
    assignments=[]
    print("DEBUG: get_courses() returned:")
    print(all_courses)
    
    for course in all_courses:
        assignments += get_assignment(course_id=course['id'],token=token)

    #update assignment in database 

    for assignment in assignments:
        try:
            # extract assignment name
            assignment_name = assignment.get("name")

            # clean description (strip HTML and keep file name/link)
            raw_description = assignment.get("description", "")
            soup = BeautifulSoup(raw_description, "html.parser")
            # get text content, e.g., file name
            description_text = soup.get_text(" ", strip=True)

            # extract course_id (to later map to course_name)
            course_id = assignment.get("course_id")

            # extract due date
            due_date = assignment.get("due_at")

            dict_assignment = {
                "title": assignment_name,
                "description": description_text,
                "course_name": get_course_by_id(course_id=course_id,token=token),
                "due_date": due_date,
                "user_id": user_id
            }
            assignment_schema=schemas.AssignmentCreate(**dict_assignment)
            crud.create_assignment(assignment=assignment_schema, db=db)
        except:
            print(assignment)

### Some assignments dont parsse


    
