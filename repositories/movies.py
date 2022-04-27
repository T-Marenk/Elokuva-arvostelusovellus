from database_connection import db

def first_page():
    sql = "SELECT name, id, year FROM movies ORDER BY id DESC limit 10"
    result = db.session.execute(sql)
    movies = result.fetchall()
    return movies

def movie(id):
    sql = "SELECT M.name, M.id, M.year, M.length, M.genre, D.description, R.review, R.id AS rid, R.stars, R.user_id, R.left_at, U.username, " \
           "(SELECT AVG(stars)::numeric(10,2) as all_stars FROM reviews WHERE movie_id=:id) FROM movies M LEFT JOIN description D ON D.movie_id = M.id " \
           "LEFT JOIN reviews R ON M.id = R.movie_id LEFT JOIN users U ON R.user_id = U.id WHERE M.id = :id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchall()
    return movie
    
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

def delete_review(review_id):
    sql = "SELECT movie_id FROM reviews WHERE id=:review_id"
    result = db.session.execute(sql, {"review_id":review_id})
    movie_id = result.fetchone()[0]
    sql = "DELETE FROM reviews WHERE id=:review_id"
    db.session.execute(sql, {"review_id":review_id})
    db.session.commit()
    return movie_id

def leave_request(movie_name, movie_year):
    sql = "INSERT INTO pending (movie_name, year) VALUES (:movie_name, :movie_year)"
    db.session.execute(sql, {"movie_name":movie_name, "movie_year":movie_year})
    db.session.commit()

def get_requests():
    sql = "SELECT * FROM pending"
    result = db.session.execute(sql)
    pending = result.fetchall()
    return pending

def delete_request(id):
    sql = "DELETE FROM pending WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()

def get_request(id):
    sql = "SELECT * FROM PENDING WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()
    return movie

def add_movie(name, year, length, genre):
    sql = "INSERT INTO movies (name, year, length, genre) VALUES (:name, :year, :length, :genre) RETURNING id"
    result = db.session.execute(sql, {"name":name, "year":year, "length":length, "genre":genre})
    movie_id = result.fetchone()[0]
    db.session.commit()
    return movie_id

def add_description(movie_id, description):
    sql = "INSERT INTO description (movie_id, description) VALUES (:movie_id, :description)"
    db.session.execute(sql, {"movie_id":movie_id, "description":description})
    db.session.commit()
