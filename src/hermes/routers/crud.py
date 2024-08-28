import logging
from typing import Iterable
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from hermes.connectors.sql_connector.database import engine
from hermes.connectors.sql_connector.schema import UserCreate
from hermes.nodes.crud import _create_user, _get_user, _get_user_by_email, _get_users
from hermes.nodes.schema import CreateUserResponse, GetUserResponse, GetUsersResponse

logger = logging.getLogger(__name__)
router = APIRouter()


def get_session() -> Iterable[Session]:
    with Session(engine) as session:
        yield session


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate, session: Session = Depends(get_session)
) -> CreateUserResponse:
    user = _get_user_by_email(session, user_create.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with the following data already exists: {user.model_dump()}",
        )

    user = _create_user(session, user_create=user_create)

    return CreateUserResponse(
        message=f"The following user is created:\n{user.model_dump()}"
    )


@router.get("/get-user/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: UUID, session: Session = Depends(get_session)) -> GetUserResponse:
    user = _get_user(session, user_id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    return GetUserResponse(message=f"Got the following user:\n{user.model_dump()}")


@router.get("/get-users", status_code=status.HTTP_200_OK)
def get_users(session: Session = Depends(get_session)) -> GetUsersResponse:
    users = _get_users(session)

    return GetUsersResponse(
        message=f"Here are all users in the database:\n{[user.model_dump() for user in users]}"
    )
