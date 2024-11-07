from sqlalchemy import ForeignKey

from database import Model
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

class FavoriteMovies(Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    kinopoisk_id: Mapped[int] = mapped_column(index=True, unique=True)
    name: Mapped[str]
    rating: Mapped[str]
    year: Mapped[str]
    description: Mapped[str]
    rating_age_limits: Mapped[str]
    genre: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Определяем отношения: один студент имеет один факультет
    user: Mapped["User"] = relationship("User", back_populates="favorite_movies")
    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"