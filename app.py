from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute("SELECT id, name FROM Movies")
    movies = result.fetchall()
    return render_template("index.html", count=len(movies), movies=movies)

@app.route("/movie/<int:id>")
def movie(id):
    sql = "SELECT name FROM Movies WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()[0]
    return render_template("movie.html", id=id, movie=movie)


