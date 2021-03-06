from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from routers import projects
from datatypes.models import *
from dependencies import *
from security.schemas import Token
from security.utils import *

app = FastAPI()

app.include_router(projects.router)


@app.on_event("startup")
def on_startup():
    """
    Called on startup, creates the database tables if they do not exist
    """
    create_db_and_tables()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session  : Session = Depends(get_session)):
    """
    Reads data from the login form and returns a token if the user is valid

    :param form_data: data sent by the client
    :param session: database session from dependencies
    :return: token
    """
    user = crud.get_user(session, form_data.username)
    if user is None \
            or \
            not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=UserBase)
def register(user: User, session: Session = Depends(get_session)):
    """
    Registers a new user

    :param user: user to add to the database
    :param session: database session from dependencies
    :return: user
    """
    if crud.get_user(session, user.user_name) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User could not be registered")
    user.password = get_password_hash(user.password)
    print(crud.get_users_count(session))
    if crud.get_users_count(session) == 0:
        user.system_permissions = [SystemPermission(permission=permission) for permission in SysPermissions]
    session.add(user)
    session.commit()
    session.refresh(user)
    if not user:
        raise HTTPException(status_code=409, detail="User could not be registered")
    return user


@app.get("/me", response_model=UserBase)
def get_current_user(user: User = Depends(get_current_active_user)):
    """
    Returns the current user

    :param user: active user from dependencies
    :return: user
    """
    return user


