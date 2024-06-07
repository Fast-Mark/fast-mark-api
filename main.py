import os
import logging
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, UploadFile, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import FileResponse, HTMLResponse
from starlette.responses import RedirectResponse

from src.autorize import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, create_new_user, \
    get_current_active_user
from src.const import BASE_PATH
from src.create_diploma.TableManager import print_excel_rows
from src.modules import Token, User, ElementsList
from src.create_diploma.save_table import save_uploaded_file

app = FastAPI()
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.mount("/authorization", StaticFiles(directory=pkg_resources.resource_filename(__name__, 'authorization')), name="authorization")
# app.include_router(
#     apiRouter,
#     prefix="/api",
# )

# @app.get("/api/.*", status_code=404, include_in_schema=False)
# def invalid_api():
#     return None

# @app.get("/.*", include_in_schema=False)
# def root():
#     return HTMLResponse(pkg_resources.resource_string(__name__, 'authorization/index.html'))


@app.get('/')
async def create_app(current_user: Annotated[User, Depends(get_current_active_user)]):
    # TODO: сделать редирект на стороне пользователя... А как сохранять jwt токен между страницами??? - просто передавать из "авторизован"
    # идея такая: я создам еще одну страницу, на которой будет проверяться авторизован пользователь или нет. Если да, то дам возможность
    if current_user.email is None:
        return FileResponse(os.path.join(BASE_PATH, ".venv/src/workspace/index.html"), media_type="text/html")
    else:
        return RedirectResponse(url="/authorization")


@app.get('/list-results')
async def read_start_page():
    pass


@app.get('/workspace')
async def read_start_page(
        current_user: Annotated[User, Depends(get_current_active_user)],
        request: Request,
        response: Response,
):
    logger = logging.getLogger("uvicorn.info")
    logger.info(request.cookies.get("Authorization"))
    if current_user.email is None:
        return RedirectResponse(url="/authorization")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )

    response.set_cookie(key="Authorization", value=f'bearer {access_token}', httponly=False,
                        domain="http://localhost:5173/")
    return HTMLResponse("src/workspace/index.html", media_type="text/html")


#  Эта функция просто возвращает страницу входа
@app.get('/authorization')
async def give_authorize_page():
    return FileResponse("src//authorization//index.html", media_type="text/html")


@app.get('/{static}')
async def give_other_statics(static: str):
    logger = logging.getLogger("uvicorn.info")
    logger.info(static + " sssss")
    if static is None:
        return FileResponse("src/authorization/index.html", media_type="text/html")
    return FileResponse(path=f"src//{static}")


@app.get('/create-user')
async def create_user(username: str, email: str, password: str):
    create_new_user(username, password, email)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/verify-user")
async def verify_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response
) -> Token:
    """
    Проверяет валидность пользователя
    :param form_data: логин и пароль пользователя
    :return: токен
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="Authorization", value=f'bearer {access_token}', httponly=False,
                        domain="http://localhost:5173/")
    return Token(access_token=access_token, token_type="bearer")


# TODO: сохранять таблицу и шрифт.
# пока что можно просто создаватоь папку пользователя и добавлять туда
@app.post('/upload-table')
async def upload_table(
        current_user: Annotated[User, Depends(get_current_active_user)], file: UploadFile, project_name: str
):
    """Получает таблицу (пока только excel) с элементами от клиента"""
    await save_uploaded_file(current_user.username, project_name, file)
    return

@app.get('/create-result')
async def create_result(
        current_user: Annotated[User, Depends(get_current_active_user)], elements: ElementsList, project_name: str
):
    await print_excel_rows(current_user.username, project_name, elements)
    return

@app.get('/download-result')
async def download_result(
        current_user: Annotated[User, Depends(get_current_active_user)], project_name: str
):
    # result = await
    return

# TODO: в будущем нужно будет сохранять названия существующих проектов пользователя
# @app.get('')
# async def create_result(current_user: Annotated[User, Depends(get_current_active_user)], json: ElementWrapper, background: UploadFile, project_name: str):
#     pass
