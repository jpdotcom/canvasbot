from pydantic import BaseModel, Json
from datetime import datetime
from typing import Any, List
class UserBase(BaseModel):
    email:str 
    password:str
class UserCreate(UserBase):
    name:str 
    
    canvas_token:str

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
    embedding : List[float]

class AssignmentResponse(AssignmentBase):

    id: int 
    user_id: int 

    class Config:
        orm_mode=True 
    
class SemanticSearchRequest(BaseModel):
    query: str
    user_id: int
    top_k: int = 3
