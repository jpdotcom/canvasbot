import requests 
import crud;
from bs4 import BeautifulSoup
import schemas
from utils.embeddings import get_embeddings

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
    url = f"{CANVAS_BASE_URL}/courses/{course_id}/assignments?per_page=100"

    resp = requests.get(url,headers=get_header(token));

    return resp.json()

def sync_assignments(user_id,db):

    token=crud.get_user_token(db=db,user_id=user_id)
    all_courses = get_courses(token=token);
    assignments=[]
    print("DEBUG: get_courses() returned:")
    print(all_courses)
    
    for course in all_courses:
        #check operating sytems class with course_id = 49756 
        #print(f"Fetching assignments for course: {course['name']} (ID: {course['id']})")
        #print assignments for debugging
        #print(get_assignment(course_id=course['id'],token=token))
        assignments += get_assignment(course_id=course['id'],token=token)

    #update assignment in database 
    #Count lost assignments
    missed_assignments=0
    for assignment in assignments:
        try:
            # extract assignment name
            assignment_name = assignment.get("name")

            # clean description (strip HTML and keep file name/link)
            raw_description = assignment.get("description", "")
            if (raw_description is None):
                raw_description=""
            soup = BeautifulSoup(raw_description, "html.parser")
            # get text content, e.g., file name
            description_text = soup.get_text(" ", strip=True)

            # extract course_id (to later map to course_name)
            course_id = assignment.get("course_id")

            # extract due date
            due_date = assignment.get("due_at")

            #get course name and embedding
            course_name = get_course_by_id(course_id=course_id,token=token)
            text = f"{course_name} {assignment_name} {description_text}"
            print("Before embedding generation for assignment:", assignment_name)
            embedding = get_embeddings(text)
            #print("Embedding generated for assignment:", assignment_name, embedding[:5], "...")
            dict_assignment = {
                "title": assignment_name,
                "description": description_text,
                "course_name": course_name,
                "due_date": due_date,
                "user_id": user_id,
                "embedding": embedding
            }
            assignment_schema=schemas.AssignmentCreate(**dict_assignment)
            crud.create_assignment(assignment=assignment_schema, db=db)
        except Exception as e:
          
            print(e)
            #print(f"Failed to parse assignment: {assignment} \n")
            missed_assignments+=1
            #print assignment title if exists 
            if 'name' in assignment:
                print(f"Failed to parse assignment: {assignment['name']}")
            else:
                print(f"Failed to parse assignment with no title")
            
            #print all other fields needed if theye exist
            if 'description' in assignment:
                print(f"Description: {assignment['description']}")
            if 'course_id' in assignment:
                print(f"Course ID: {assignment['course_id']}")
            if 'due_at' in assignment:
                print(f"Due Date: {assignment['due_at']}")
    print(f"Missed {missed_assignments} assignments during sync.")

### Some assignments dont parsse



    
