
from pydantic import EmailStr
import bcrypt
from sqlalchemy.orm import Session

from hermes.connectors.sql_connector import schemas, models


def get_hashed_password(password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_create: schemas.UserCreate):
    hashed_password = get_hashed_password(user_create.password)
    db_user = models.User(email=user_create.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_user_item(db: Session, item_create: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item_create.model_dump(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()
