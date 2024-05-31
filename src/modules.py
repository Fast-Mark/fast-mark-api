from typing import List

from pydantic import BaseModel, Field, validator


class Element(BaseModel):
    position: str | None = "center"
    font_family: str | None = "Arial"
    font_size: int | None = 18
    font_color: str | None = "#000000"
    # TODO: сделать константы как во фронте
    font_style: str | None = "basic"


class ElementWrapper(BaseModel):
    key: str | None
    poistion_x: str | None = "0px"
    position_y: str | None = "0px"
    width: str | None = "0px"
    height: str | None = "0px"
    aligment: str = Field()
    element: Element

    # @validator('alignment')
    # def validate_alignment(cls, value):
    #     allowed_values = {'left', 'right', 'center'}
    #     if value not in allowed_values:
    #         raise ValueError(f'alignment must be one of {allowed_values}, not {value}')
    #     return value


class ElementsList(BaseModel):
    elements: List[Element]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

    @classmethod
    def from_db_row(cls, row):
        """
        Создает экземпляр класса UserInDB из строки результата запроса.
        """
        return cls(
            username=row[0],
            email=row[2],
            disabled=row[3],
            hashed_password=row[1]
        )


class UserAutorize(BaseModel):
    email: str | None = None
    password: str | None = None
