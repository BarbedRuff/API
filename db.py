from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Column
from sqlalchemy import create_engine
from sqlalchemy import select, insert, update, delete
from config import DATABASE_NAME_COLUMNS as columns
from uuid import uuid4
import json


class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = 'movies'
    id = Column("id", String, primary_key=True)
    title = Column("title", String(100))
    year = Column("year", Integer)
    director = Column("director", String(100))
    length = Column("length", Integer)
    rating = Column("rating", Integer)

class EngineWorker:
    def __init__(self, path):
        self.engine = create_engine(path)

    def moviesList(self):
        stmt = select(Movie)
        movies_list = []
        with self.engine.connect() as conn:
            movies = conn.execute(stmt).all()
            conn.commit()
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
        
    def findMovie(self, movie_id):
        id = hex(movie_id)[2:]
        stmt = select(Movie).where(Movie.id == id)
        with self.engine.connect() as conn:
            movie = conn.execute(stmt).first()
            conn.commit()
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
                raise Exception('Not found movie')
    
    def pathcMovie(self, movie_id, movie):
        id = hex(movie_id)[2:]
        stmt = update(Movie).\
            where(Movie.id == id).\
                values(
                    id=id,
                    title=movie[columns[1]],
                    year=movie[columns[2]],
                    director=movie[columns[3]],
                    length=movie[columns[4]],
                    rating=movie[columns[5]]
                ).returning(Movie.id)
        with self.engine.connect() as conn:
            patched_id = conn.execute(stmt).first()
            conn.commit()
            if patched_id is not None: 
                return json.dumps(
                    {"movie": {
                        "id": movie_id,
                        "title":movie[columns[1]],
                        "year":movie[columns[2]],
                        "director":movie[columns[3]],
                        "length":movie[columns[4]],
                        "rating":movie[columns[5]]
                    }}
                )    
            else:
                raise Exception('Not found movie')
    
    def deleteMovie(self, movie_id):
        id = hex(movie_id)[2:]
        stmt = delete(Movie).\
            where(Movie.id == id).\
                returning(Movie.id)
        with self.engine.connect() as conn:
            deleted_id = conn.execute(stmt).first()
            conn.commit()
            if deleted_id is not None: 
                return "Deleted"
            else:
                raise Exception('Not found movie')
