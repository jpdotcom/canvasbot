from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
import db 
import schemas
import crud 
import canvas_api
router = APIRouter(prefix='/assignments', tags=["assignments"]) 
TOKEN = "5590~6tU2ynHJGBhXynfDYFGAKfznJFYrQU2tPJUr3m273cvx8NAz88CQEnAFG6DFER9D"


@router.post("/",response_model=schemas.AssignmentResponse)
def create_assignment(assignment:schemas.AssignmentCreate, database: Session = Depends(db.get_db)):
    return crud.create_assignment(assignment=assignment,db=database)

@router.get("/{assignment_id}",response_model=schemas.AssignmentResponse)
def get_assignment(assignment_id: int, database: Session = Depends(db.get_db)):
    assignment = crud.get_assignment(assignment_id=assignment_id,db=database);
    if assignment is None: 
        raise HTTPException(status_code=404,detail="Assignment Not Found" )
        return 
    return assignment;

@router.post("/sync/{user_id}")
def sync(user_id:int,database:Session=Depends(db.get_db)):
    canvas_api.sync_assignments(user_id=user_id,db=database,token=TOKEN);
    return;