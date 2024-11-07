from dao.base import BaseDAO
from database import async_session_maker
from movies.models import FavoriteMovies
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

class FavoriteMoviesDAO(BaseDAO):
    model = FavoriteMovies

    @classmethod
    async def find_favorite_movies(cls, user_id):
        async with async_session_maker() as session:
            print('fjsdkfjlksdjflksd')
            query = select(cls.model).options(joinedload(cls.model.user)).filter_by(user_id=int(user_id))
            result = await session.execute(query)
            favorite_movies_info = result.scalars().all()

            result_dicts = [{column.name: getattr(row, column.name) for column in FavoriteMovies.__table__.columns}
                            for row in favorite_movies_info]
            return result_dicts