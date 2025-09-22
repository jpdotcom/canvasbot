from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
import db 
import schemas
import crud
router = APIRouter(prefix='/users', tags=["users"]) 

@router.post("/", response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,database:Session = Depends(db.get_db)):
    return crud.create_user(database,user) 


@router.get("/{user_id}",response_model=schemas.UserResponse)
def read_user(user_id:int, database: Session = Depends(db.get_db)):
    user=crud.get_user(database,user_id)
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user 

@router.post("/validate")
def validate_user(user:schemas.UserBase, database:Session = Depends(db.get_db)):
    print("HELLO")
    user = crud.get_user_by_login(user,db=database);
    if (user):
        return "200"
    raise HTTPException(status_code=404, detail="Email is incorrect or password is incorrect");

    
