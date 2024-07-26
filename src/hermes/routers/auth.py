from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from hermes.connectors.sql_connector.database import SessionLocal
from hermes.connectors.sql_connector.schemas import TokenType, UserCreate
from hermes.nodes.crud import get_user_by_email, verify_password
from hermes.nodes.schema import LoginResponse


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
router = APIRouter()

@router.post("/login/", status_code=status.HTTP_200_OK)
def login(user_create: UserCreate, db: Session = Depends(get_db)) -> LoginResponse:
    db_user = get_user_by_email(db=db, email=user_create.email)
    if not db_user or not verify_password(user_create.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # TODO: Replace this fake token with JWT token
    return LoginResponse(access_token='fake-jwt-token', token_type=TokenType.bearer)
