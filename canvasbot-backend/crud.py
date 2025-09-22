from sqlalchemy.orm import Session 
import models,schemas 

def create_user(db:Session, user:schemas.UserCreate):

    db_user = models.User(name=user.name,email=user.email,canvas_token=user.canvas_token,password=user.password)

    db.add(db_user);
    db.commit() 
    db.refresh(db_user);
    return db_user;
def get_user(db:Session,user_id:int):
    return db.query(models.User).filter(models.User.id == user_id).first();

def get_user_by_login(user:schemas.UserCreate, db:Session):
    
    found_user = db.query(models.User).filter(models.User.email == user.email).first();
    if (found_user and user.password == found_user.password):
        return True;
    else:
        return False;

def create_assignment(assignment:schemas.AssignmentCreate,db:Session):

    db_assignment = models.Assignment(user_id=assignment.user_id, course_name = assignment.course_name, title = assignment.title, description = assignment.description, due_date=assignment.due_date)
    db.add(db_assignment);
    db.commit();
    db.refresh(db_assignment);
    return db_assignment

def get_assignment(assignment_id: int, db:Session):
    return db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()


def get_user_token(db:Session, user_id:int):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if (user):
        return user.canvas_token;
    return None;