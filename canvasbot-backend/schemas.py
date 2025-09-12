from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email:str 

class UserCreate(UserBase):
    name:str 


class UserResponse(UserBase):
    id: int
    name: str 

    class Config:
        orm_mode = True 


class AssignmentBase(BaseModel):

    course_name : str 
    title : str
    description : str
    due_date : datetime 

class AssignmentCreate(AssignmentBase):
    user_id : int


class AssignmentResponse(AssignmentBase):

    id: int 
    user_id: int 

    class Config:
        orm_mode=True 
    
