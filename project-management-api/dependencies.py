# Dependency
import enum
import json.decoder
from datetime import timedelta, datetime
from typing import Dict

import yaml
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate
from sqlmodel import create_engine, SQLModel, Session
from starlette.requests import Request

from app_config import SECRET_KEY
from auth import Permissions, has_document_permission, has_project_permission, has_system_user_permission
from database import crud
from datatypes.models import User, DocPermissions, Document, DocumentRole, ProjPermissions, Project
from security.schemas import TokenData
from security.utils import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
sqlite_file_name = "./db/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token  : str     = Depends(oauth2_scheme),
                           session: Session = Depends(get_session)):\

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


def get_project(
        project_name: str | None = None,
        session: Session = Depends(get_session)):
    if project_name is None:
        return None
    db_project = crud.get_project_by_name(session, project_name)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project


def get_document(project_name : str | None = None,
                 document_name: str | None = None,
                 session      : Session    = Depends(get_session)):
    if document_name is None:
        return None
    db_doc = crud.get_document_of_project(session, project_name, document_name)
    if db_doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return db_doc


class CheckDocumentPermission:
    def __init__(self, permission: Permissions):
        self.permission = permission

    def __call__(self,
                 session   : Session  = Depends(get_session),
                 user      : User     = Depends(get_current_active_user),
                 db_project: Project  = Depends(get_project),
                 db_doc    : Document = Depends(get_document)):
        if not has_document_permission(session,
                                       user,
                                       db_project,
                                       db_doc,
                                       self.permission):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def require_document_permission(permission: Permissions):
    return CheckDocumentPermission(permission)


class CheckProjectPermission:
    def __init__(self, permission: Permissions):
        self.permission = permission

    def __call__(self,
                 session   : Session        = Depends(get_session),
                 user      : User           = Depends(get_current_active_user),
                 db_project: Project | None = Depends(get_project)):

        if not has_project_permission(session, user, db_project, self.permission):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def require_project_permission(permission: Permissions):
    return CheckProjectPermission(permission)


class CheckSystemPermission:
    def __init__(self, permission: Permissions):
        self.permission = permission

    def __call__(self,
                 session: Session = Depends(get_session),
                 user   : User    = Depends(get_current_active_user)):
        if not has_system_user_permission(session, user, self.permission):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def require_system_permission(permission: Permissions):
    return CheckSystemPermission(permission)


async def get_request_body(request: Request):
    if "content-type" not in request.headers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Content-Type in header")
    content_type = request.headers['content-type']

    match content_type:
        case "application/json":
            try:
                request_body = await request.json()
            except json.decoder.JSONDecodeError as err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
        case "application/x-yaml":
            try:
                request_body = yaml.safe_load(await request.body())
            except Exception as err:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
        case _:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return request_body


def check_document_process(db_doc: Document = Depends(get_document)):
    for process_document in db_doc.documents_processes:
        if process_document.document_role == DocumentRole.output:
            if any(bool(document_process.document.first) is False for document_process in
                   process_document.process.documents_processes if
                   document_process.document_role == DocumentRole.input):
                raise HTTPException(status_code=status.HTTP_428_PRECONDITION_REQUIRED,
                                    detail="Process requirements not satisfied")


def validate_document(db_doc: Document = Depends(get_document),
                      document_body: Dict = Depends(get_request_body)):
    try:
        validate(document_body, db_doc.jsonschema)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
