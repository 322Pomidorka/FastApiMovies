from pydantic import BaseModel, Field


class SUserRegister(BaseModel):
    login_name: str = Field(..., description="Логин")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")


class SUserAuth(BaseModel):
    login_name: str = Field(..., description="Логин")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")