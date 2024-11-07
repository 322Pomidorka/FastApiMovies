from fastapi import APIRouter, HTTPException, status, Response
from fastapi.params import Depends

from users.dao import UsersDAO
from users.dependencies import get_current_user
from users.shemas import SUserRegister, SUserAuth
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.models import User

router = APIRouter(tags=['Auth'])


@router.post("/register/", summary="Регистрация нового пользователя с указанием имени пользователя и пароля")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(login_name=user_data.login_name)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': f'Вы успешно зарегистрированы!'}


@router.post("/login/", summary='Аутентификация пользователя и получение JWT токена')
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(login_name=user_data.login_name, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'Авторизация успешна!'}


@router.get("/profile/", summary='Получение информации о текущем аутентифицированном пользователе')
async def profile(user_data: User = Depends(get_current_user)):
    return {'login': user_data.login_name, 'first_name': user_data.first_name, 'last_name': user_data.last_name}
