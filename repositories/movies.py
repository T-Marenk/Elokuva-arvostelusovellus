from database_connection import db

def first_page():
    sql = "SELECT name, id, year FROM movies ORDER BY id DESC limit 10"
    result = db.session.execute(sql)
    movies = result.fetchall()
    return movies

def movie(id):
    sql = "SELECT M.name, M.id, M.year, M.length, M.genre, D.description FROM movies M LEFT JOIN description D ON D.movie_id = M.id WHERE M.id = :id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()
    return movie

def reviews(id):
    sql = "SELECT A.stars, A.user_id, A.review, A.left_at, U.username FROM reviews A, users U WHERE A.movie_id=:id AND A.user_id=U.id"
    result = db.session.execute(sql, {"id":id})
    reviews = result.fetchall()
    return reviews

def stars(id):
    sql = "SELECT ROUND(SUM(stars)/COUNT(*),1) FROM reviews WHERE movie_id=:id"
    result = db.session.execute(sql, {"id":id})
    all_stars = result.fetchone()
    return all_stars
    
def search_movies_name(name):
    sql = "SELECT id, name, year, genre FROM movies WHERE name LIKE :name"
    result = db.session.execute(sql, {"name":"%"+name+"%"})
    movies = result.fetchall()
    return movies

def search_movies_genre(genre):
    sql = "SELECT id, name, year, genre FROM movies WHERE genre LIKE :genre"
    result = db.session.execute(sql, {"genre":"%"+genre+"%"})
    movies = result.fetchall()
    return movies

def leave_review(movie_id, stars, review, user_id):
    sql = "INSERT INTO reviews (movie_id, stars, review, left_at, user_id) VALUES (:movie_id, :stars, :review, NOW(), :user_id)"
    db.session.execute(sql, {"movie_id":movie_id, "stars":stars, "review":review, "user_id":user_id})
    db.session.commit()
