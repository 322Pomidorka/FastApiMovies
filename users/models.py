from database import Model
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
from movies.models import FavoriteMovies


class User(Model):
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    login_name: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]

    # Определяем отношения: один пользователь может иметь много фильмов
    favorite_movies: Mapped[list["FavoriteMovies"]] = relationship("FavoriteMovies", back_populates="user")



    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"