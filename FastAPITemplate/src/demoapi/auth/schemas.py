from typing import Optional, List
from pydantic import BaseModel, model_validator, EmailStr

from demoapi.core.role import Role


class LoginSchema(BaseModel):

    login: str
    password: str


class RegisterSchema(BaseModel):  # TODO: На усмотрение системы

    phone: str
    email: str
    surname: str
    name: str
    patronymic: str
    password: str
    social_link: str
