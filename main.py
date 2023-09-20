from flask import Flask, request, abort, Response
from db import EngineWorker
from config import DATABASE_PATH as dbpath, DATABASE_NAME_COLUMNS as columns


app = Flask(__name__)
engworker = EngineWorker(dbpath)

def check_movie(movie):
    if len(movie[columns[1]]) > 100 or len(movie[columns[1]]) == 0:
        return Response(response="Title string length greater than 100 or equal to 0", status=500)
    elif not(1900 <= movie[columns[2]] <= 2100):
        return Response(response="Year not in range 1900...2100", status=500)
    elif len(movie[columns[3]]) > 100 or len(movie[columns[3]]) == 0:
        return Response(response="Director string greater than 100 or equal to 0", status=500)
    elif not(0 <= movie[columns[5]] <= 10):
        return Response(response="Rating not in range 0...10", status=500)


@app.route("/api/movies", methods=["GET"])
def get_all_movies():
    return engworker.moviesList()

@app.route("/api/movies",  methods=["POST"])
def add_movie():
    movie = request.get_json()['movie']
    checked = check_movie(movie)
    if checked is not None:
        return checked
    try:
        return engworker.addMovie(movie)
    except Exception as e:
        return Response(response=str(e), status=500)

@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def find_movie_by_id(movie_id):
    try:
        return engworker.findMovie(movie_id)
    except Exception: 
        return Response(response="Movie not found", status=404)
        
@app.route("/api/movies/<int:movie_id>", methods=["PATCH"])
def patch_movie_by_id(movie_id):
    movie = request.get_json()['movie']
    checked = check_movie(movie)
    if checked is not None:
        return checked
    try:
        return engworker.pathcMovie(movie_id, movie)
    except Exception as e:
        return Response(response=str(e), status=500)
        
@app.route("/api/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie_by_id(movie_id):
    return engworker.deleteMovie(movie_id)
