from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
import db 
import schemas
import crud
router = APIRouter(prefix='/users', tags=["users"]) 

@router.post("/",response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,database:Session = Depends(db.get_db)):

    existing_user = crud.get_user_by_email(db=database,email=user.email);
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
        
    return crud.create_user(database,user) 


@router.get("/{user_id}",response_model=schemas.UserResponse)
def read_user(user_id:int, database: Session = Depends(db.get_db)):
    user=crud.get_user(database,user_id)
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user 

@router.post("/validate",response_model=schemas.UserResponse)
def validate_user(user:schemas.UserBase, database:Session = Depends(db.get_db)):
    user = crud.get_user_by_login(user,db=database);
    if (user):
        #turn user into json 
        return user
    raise HTTPException(status_code=404, detail="Email is incorrect or password is incorrect");

@router.get("/by_email/{email}",response_model=schemas.UserResponse)
def get_user_by_email(email:str, database:Session = Depends(db.get_db)):
    
    user = crud.get_user_by_email(db=database,email=email);
    if (user):
        return user
    raise HTTPException(status_code=404, detail="User not found");
