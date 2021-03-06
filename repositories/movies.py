from database_connection import db

def first_page():
    sql = "SELECT name, id, year FROM movies ORDER BY id DESC limit 10"
    result = db.session.execute(sql)
    movies = result.fetchall()
    return movies

def movie(id):
    sql = "SELECT DISTINCT(R.user_id), M.name, M.id, M.year, M.length, M.genre, D.description, R.review, R.id AS rid, R.stars, R.left_at, U.username, " \
           "(SELECT AVG(stars)::numeric(10,2) as all_stars FROM reviews WHERE movie_id=:id) FROM movies M LEFT JOIN description D ON D.movie_id = M.id " \
           "LEFT JOIN reviews R ON M.id = R.movie_id LEFT JOIN users U ON R.user_id = U.id WHERE M.id = :id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchall()
    return movie

def platforms(id):
    sql = "SELECT DISTINCT(P.link), P.name, P.id FROM platforms P LEFT JOIN view_at V ON P.id = V.platform_id WHERE V.movie_id = :id"
    result = db.session.execute(sql, {"id":id})
    platforms = result.fetchall()
    return platforms

def all_platforms():
    sql = "SELECT DISTINCT(name), id, link FROM platforms"
    result = db.session.execute(sql)
    all_platforms = result.fetchall()
    return all_platforms

def add_movie_platform(platform_id, movie_id):
    sql = "INSERT INTO view_at (movie_id, platform_id) VALUES (:movie_id, :platform_id)"
    db.session.execute(sql, {"movie_id":movie_id, "platform_id":platform_id})
    db.session.commit()

def add_platform(platform_name, platform_link):
    sql = "INSERT INTO platforms (name, link) VALUES (:name, :link)"
    db.session.execute(sql, {"name":platform_name, "link":platform_link})
    db.session.commit()

def delete_movie_platform(movie_id, platform_id):
    sql = "DELETE FROM view_at WHERE movie_id=:movie_id AND platform_id=:platform_id"
    db.session.execute(sql, {"movie_id":movie_id, "platform_id":platform_id})
    db.session.commit()

def delete_all_movie_platforms(movie_id):
    sql = "DELETE FROM view_at WHERE movie_id=:movie_id"
    db.session.execute(sql, {"movie_id":movie_id})
    db.session.commit()

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

def delete_movie_reviews(movie_id):
    sql = "DELETE FROM reviews WHERE movie_id=:movie_id"
    db.session.execute(sql, {"movie_id":movie_id})
    db.session.commit()

def delete_description(movie_id):
    sql = "DELETE FROM description WHERE movie_id=:movie_id"
    db.session.execute(sql, {"movie_id":movie_id})
    db.session.commit()

def delete_movie(movie_id):
    sql = "DELETE FROM movies WHERE id=:movie_id"
    db.session.execute(sql, {"movie_id":movie_id})
    db.session.commit()
    
def leave_request(movie_name, movie_year):
    try:
        int(movie_year)
    except:
        return movie_name, movie_year, False
    sql = "INSERT INTO pending (movie_name, year) VALUES (:movie_name, :movie_year)"
    db.session.execute(sql, {"movie_name":movie_name, "movie_year":movie_year})
    db.session.commit()
    return movie_name, movie_year, True

def get_requests():
    sql = "SELECT DISTINCT(movie_name), id, year FROM pending"
    result = db.session.execute(sql)
    pending = result.fetchall()
    return pending

def delete_request(id, movie_name):
    sql = "DELETE FROM pending WHERE id=:id OR movie_name=:movie_name"
    db.session.execute(sql, {"id":id, "movie_name":movie_name})
    db.session.commit()

def get_request(id):
    sql = "SELECT DISTINCT(movie_name), id, year FROM PENDING WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()
    return movie

def add_movie(name, year, length, genre):
    sql = "INSERT INTO movies (name, year, length, genre) VALUES (:name, :year, :length, :genre) RETURNING id, name"
    result = db.session.execute(sql, {"name":name, "year":year, "length":length, "genre":genre})
    movie = result.fetchone()
    db.session.commit()
    return movie[0], movie[1]

def add_description(movie_id, description):
    sql = "INSERT INTO description (movie_id, description) VALUES (:movie_id, :description)"
    db.session.execute(sql, {"movie_id":movie_id, "description":description})
    db.session.commit()
