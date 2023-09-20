from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Column
from sqlalchemy import create_engine
from sqlalchemy import select, insert
from uuid import uuid4
from config import DATABASE_NAME_COLUMNS as columns
import json


class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(String, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    director = Column(String)
    length = Column(Integer)
    rating = Column(Integer)

class EngineWorker:
    def __init__(self, path):
        self.engine = create_engine(path)

    def moviesList(self):
        stmt = select(Movie)
        movies_list = []
        with self.engine.connect() as conn:
            movies = conn.execute(stmt).all()
            movies_list = [
                {
                    "id": int(movie[0], 16),
                    "title": movie[1],
                    "year": movie[2],
                    "director": movie[3],
                    "length": movie[4],
                    "rating": movie[5]
                }
                for movie in movies
            ]
        return json.dumps({"list": movies_list})
        
    def addMovie(self, movie):
        id = uuid4().hex
        stmt = insert(Movie).values(
            id=id,
            title=movie[columns[1]],
            year=movie[columns[2]],
            director=movie[columns[3]],
            length=movie[columns[4]],
            rating=movie[columns[5]]
        )
        try:
            with self.engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()
            return json.dumps(
                {"movie": {
                    "id": int(id, 16),
                    "title":movie[columns[1]],
                    "year":movie[columns[2]],
                    "director":movie[columns[3]],
                    "length":movie[columns[4]],
                    "rating":movie[columns[5]]
                }}
            )
        except Exception as e:
            raise e
        
    def find_movie(self, movie_id):
        id = hex(movie_id)[2:]
        stmt = select(Movie).where(Movie.id == id)
        with self.engine.connect() as conn:
            movie = conn.execute(stmt).first()
            if movie is not None:
                return json.dumps(
                    {"movie": {
                        "id": movie_id,
                        "title":movie[1],
                        "year":movie[2],
                        "director":movie[3],
                        "length":movie[4],
                        "rating":movie[5]
                    }}
                )
            else:
                raise Exception('not found user')
            