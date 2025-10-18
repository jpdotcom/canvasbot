from sqlalchemy.orm import Session 
from datetime import datetime
import models, schemas
import os
from cryptography.fernet import Fernet

# Encryption setup
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY").encode()
cipher = Fernet(ENCRYPTION_KEY)

def decrypt(encrypted_text: str) -> str:
    """Decrypt Canvas token"""
    if encrypted_text is None:
        return None
    return cipher.decrypt(encrypted_text.encode()).decode()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        canvas_token=None  # Will be encrypted and added separately
    )
    
    db.add(db_user)
    db.commit() 
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_login(user: schemas.UserCreate, db: Session):
    found_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if (found_user and user.password == found_user.password):
        return found_user
    else:
        return None

def update_canvas_token(db: Session, user_id: int, canvas_token: str):
    """Update user's Canvas token (should already be encrypted when passed in)"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.canvas_token = canvas_token
        db.commit()
        db.refresh(user)
    return user

def create_assignment(assignment: schemas.AssignmentCreate, db: Session):
    db_assignment = models.Assignment(
        user_id=assignment.user_id, 
        course_name=assignment.course_name, 
        title=assignment.title, 
        description=assignment.description, 
        due_date=assignment.due_date, 
        embedding=assignment.embedding
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def get_assignment(assignment_id: int, db: Session):
    return db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()

def get_user_token(db: Session, user_id: int):
    """Get and decrypt user's Canvas token"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if (user and user.canvas_token):
        return decrypt(user.canvas_token)  # Decrypt before returning
    return None

def get_all_assignments_by_user(user_id: int, db: Session):
    return db.query(models.Assignment).filter(models.Assignment.user_id == user_id).all()

def remove_assignment(assignment_id: int, db: Session):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if assignment:
        db.delete(assignment)
        db.commit()
    return

def get_all_current_assignments_by_user(user_id: int, db: Session):
    return db.query(models.Assignment).filter(models.Assignment.due_date >= datetime.now())