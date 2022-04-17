from database_connection import db

def search_movies_name(name):
    sql = "SELECT M.id, M.name, I.year, I.genre FROM movies M LEFT JOIN information I ON I.movie_id = M.id WHERE M.name LIKE :name"
    result = db.session.execute(sql, {"name":"%"+name+"%"})
    movies = result.fetchall()
    return movies

def search_movies_genre(genre):
    sql = "SELECT M.id, M.name, I.year, I.genre FROM movies M LEFT JOIN information I ON I.movie_id = M.id WHERE I.genre LIKE :genre"
    result = db.session.execute(sql, {"genre":"%"+genre+"%"})
    movies = result.fetchall()
    return movies
