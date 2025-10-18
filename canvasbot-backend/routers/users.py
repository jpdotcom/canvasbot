from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
import db 
import schemas
import crud
import os
from cryptography.fernet import Fernet

router = APIRouter(prefix='/users', tags=["users"]) 

# Encryption setup
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()
cipher = Fernet(ENCRYPTION_KEY)

def encrypt(text: str) -> str:
    """Encrypt Canvas token"""
    if text is None:
        return None
    return cipher.encrypt(text.encode()).decode()

def decrypt(encrypted_text: str) -> str:
    """Decrypt Canvas token"""
    if encrypted_text is None:
        return None
    return cipher.decrypt(encrypted_text.encode()).decode()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, database: Session = Depends(db.get_db)):
    existing_user = crud.get_user_by_email(db=database, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Encrypt canvas_token if provided
    encrypted_token = None
    if hasattr(user, 'canvas_token') and user.canvas_token:
        encrypted_token = encrypt(user.canvas_token)
    
    # Create user with encrypted token
    db_user = crud.create_user(database, user)
    
    # If token was provided, update it with encrypted version
    if encrypted_token:
        crud.update_canvas_token(database, db_user.id, encrypted_token)
    
    return db_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, database: Session = Depends(db.get_db)):
    user = crud.get_user(database, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user 

@router.post("/validate", response_model=schemas.UserResponse)
def validate_user(user: schemas.UserBase, database: Session = Depends(db.get_db)):
    user = crud.get_user_by_login(user, db=database)
    if (user):
        return user
    raise HTTPException(status_code=404, detail="Email is incorrect or password is incorrect")

@router.get("/by_email/{email}", response_model=schemas.UserResponse)
def get_user_by_email(email: str, database: Session = Depends(db.get_db)):
    user = crud.get_user_by_email(db=database, email=email)
    if (user):
        return user
    raise HTTPException(status_code=404, detail="User not found")

# New endpoint to manually update Canvas token
@router.post("/{user_id}/canvas_token")
def update_user_canvas_token(user_id: int, canvas_token: str, database: Session = Depends(db.get_db)):
    """Endpoint for users to manually add/update their Canvas token"""
    user = crud.get_user(database, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Encrypt the token before saving
    encrypted_token = encrypt(canvas_token)
    crud.update_canvas_token(database, user_id, encrypted_token)
    
    return {"status": "Canvas token updated successfully"}