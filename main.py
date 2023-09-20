from flask import Flask, request, abort, render_template
from db import EngineWorker
from config import DATABASE_PATH as dbpatg


app = Flask(__name__)
engworker = EngineWorker(dbpatg)


@app.route("/api/movies", methods=["GET"])
def get_all_movies():
    return engworker.moviesList()

@app.route("/api/movies",  methods=["POST"])
def add_movie():
    try:
        movie = request.get_json()['movie']
        return engworker.addMovie(movie)
    except Exception as e:
        return render_template(f'{ "status": 500, "reason": "{e}"}', e=500)

@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def find_movie_by_id(movie_id):
    try:
        return engworker.find_movie(movie_id)
    except Exception: 
        abort(404)
        
