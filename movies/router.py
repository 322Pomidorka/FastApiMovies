from fastapi import APIRouter, HTTPException, status, Response, Depends

from httpxrr.singleOnHttpx import Singletonhttpx
from movies.dao import FavoriteMoviesDAO
from users.dependencies import valid_token
from users.models import User

router = APIRouter(prefix='/movies', tags=['movies'])


@router.get("/search_query=", summary='''Ищет фильмы по названию, используя эндпойнт:-
                                               GET /api/v2.1/films/search-by-keyword'''
            )
async def get_movie_by_name(name_movie: str, page: int = 1, user_id: User = Depends(valid_token)) -> dict:
    url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={name_movie}&page={int(page)}'
    print(url)
    return await Singletonhttpx.query_url(url)


@router.get("/favorites", summary='Возвращает список избранных фильмов пользователя с подробной информацией!')
async def get_favorites_movies(user_id: User = Depends(valid_token)) -> dict:
    favorites_movies = await FavoriteMoviesDAO.find_favorite_movies(user_id=int(user_id))
    if not favorites_movies:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='У вас нет любимых фильмов'
        )
    return {'favorites_movies': favorites_movies}


@router.get("/{kinopoisk_id}", summary='''Получает подробную информацию о фильме по его Kinopoisk ID,
                                                используя эндпойнт: - GET /api/v2.2/films/{kinopoisk_id}''')
async def get_movie_info_by_kinopoisk_id(kinopoisk_id: str, user_id: User = Depends(valid_token)) -> dict:
    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{kinopoisk_id}'
    return await Singletonhttpx.query_url(url)


@router.post("/favorites", summary='Добавляет фильм в список избранных пользователя по Kinopoisk ID')
async def add_favorite_movie(kinopoisk_id: str, user_id: User = Depends(valid_token)) -> dict:
    favorite_movie = await FavoriteMoviesDAO.find_one_or_none(kinopoisk_id=kinopoisk_id)
    if favorite_movie:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Фильм уже добавлен в любимые'
        )
    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{kinopoisk_id}'
    movies_data = await Singletonhttpx.query_url(url)
    movies_dict = { 'kinopoisk_id': movies_data['kinopoiskId'],
                    'name': movies_data['nameRu'],
                    'rating': movies_data['ratingKinopoisk'],
                    'year': movies_data['year'],
                    'description': movies_data['shortDescription'],
                    'rating_age_limits': movies_data['ratingAgeLimits'],
                    'genre': movies_data['genres'][0]['genre'],
                    'user_id': user_id
                    }
    print(movies_dict)
    await FavoriteMoviesDAO.add(**movies_dict)
    return {'message': f'Фильм добавлен в любимые'}


@router.delete("/favorites/{kinopoisk_id}", summary='Удаляет фильм из списка избранных пользователя')
async def delete_movies(kinopoisk_id: str, user_id: User = Depends(valid_token)) -> dict:
    check = await FavoriteMoviesDAO.delete(kinopoisk_id=kinopoisk_id)
    if check:
        return {"message": f"Фильм с ID {kinopoisk_id} удален!"}
    else:
        return {"message": "Ошибка при удалении фильма!"}