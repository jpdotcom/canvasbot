from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
import db 
import schemas
import crud 
import canvas_api
from dotenv import load_dotenv 
import os 
from utils.auth import verify_token
router = APIRouter(prefix='/assignments', tags=["assignments"]) 


@router.post("/",response_model=schemas.AssignmentResponse)
# def create_assignment(assignment:schemas.AssignmentCreate, database: Session = Depends(db.get_db)):
#     return crud.create_assignment(assignment=assignment,db=database)
@router.get("/all",response_model=list[schemas.AssignmentResponse]) 
def get_assignments_by_user(user_id:int = Depends(verify_token), database: Session = Depends(db.get_db)):
     
    assigments = crud.get_all_assignments_by_user(user_id=user_id,db=database); 

    return assigments;
# @router.get("/{assignment_id}",response_model=schemas.AssignmentResponse)
# def get_assignment(assignment_id: int, database: Session = Depends(db.get_db)):
#     assignment = crud.get_assignment(assignment_id=assignment_id,db=database);
#     if assignment is None: 
#         raise HTTPException(status_code=404,detail="Assignment Not Found" )
#         return 
#     return assignment;


@router.post("/sync")
def sync(user_id:int = Depends(verify_token),database:Session=Depends(db.get_db)):
    #remove all assignments for user 
    assignments = crud.get_all_assignments_by_user(user_id=user_id,db=database);
    for assignment in assignments:
        crud.remove_assignment(assignment_id=assignment.id,db=database);
    
    canvas_api.sync_assignments(user_id=user_id,db=database);
    return;


