from app import app
from components.users import is_user, is_admin
from components.movies import search_movies_name, search_movies_genre
from database_connection import db
from flask import redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import string
import secrets

@app.route("/")
def index():
    sql = "SELECT M.id, M.name, I.year FROM Movies M LEFT JOIN information I on I.movie_id = M.id ORDER BY M.id DESC limit 10"
    result = db.session.execute(sql)
    movies = result.fetchall()
    return render_template("index.html", movies=movies)

@app.route("/movie/<int:id>")
def movie(id):
    sql = "SELECT M.name, M.id, I.year, I.length, I.genre, D.description FROM Movies M LEFT JOIN information I on I.movie_id = M.id " \
            "LEFT JOIN description D ON M.id = D.movie_id WHERE M.id=:id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()
    sql = "SELECT A.stars, A.user_id, A.review, A.left_at, U.username FROM reviews A, users U WHERE A.movie_id=:id AND A.user_id=U.id"
    result = db.session.execute(sql, {"id":id})
    reviews = result.fetchall()
    sql = "SELECT ROUND(SUM(stars)/COUNT(*),1) FROM reviews WHERE movie_id=:id"
    result = db.session.execute(sql, {"id":id})
    all_stars = result.fetchone()
    return render_template("movie.html", id=id, movie=movie, reviews=reviews, all_stars=all_stars)

@app.route("/search_result", methods=["GET"])
def search_result():
    search_by = request.args["search_by"]
    query = request.args["query"]
    if search_by == "name":
        movies = search_movies_name(query)
        return render_template("search_result.html", movies=movies)
    if search_by == "genre":
        movies = search_movies_genre(query)
        return render_template("search_result.html", movies=movies)

@app.route("/new_review/<int:id>")
def new_review(id):
    if is_user():
        sql = "SELECT name FROM Movies WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        movie = result.fetchone()
        username = session['username']
        sql = "SELECT id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username":username})
        user_id = result.fetchone()[0]
        return render_template("new_review.html", id=id, movie=movie, user_id=user_id)
    return render_template("new_review.html")

@app.route("/leave_review", methods=["POST"])
def leave_review():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    movie_id = request.form["id"]
    if "stars" not in request.form:
        flash("Anna elokuvalle arvostelu")
        return redirect("/new_review/" + str(movie_id))
    stars = request.form["stars"]
    review = request.form["review"]
    user_id = request.form["user_id"]
    sql = "INSERT INTO reviews (movie_id, stars, review, left_at, user_id) VALUES (:movie_id, :stars, :review, NOW(), :user_id)"
    db.session.execute(sql, {"movie_id":movie_id, "stars": stars, "review":review, "user_id":user_id})
    db.session.commit()
    return redirect("/movie/" + str(movie_id))

@app.route("/login",methods=["GET", "POST"])
def login():
    if is_user():
        return redirect("/")
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        sql = "SELECT id, password FROM users WHERE LOWER(username)=LOWER(:username)"
        result = db.session.execute(sql, {"username":username})
        user = result.fetchone()
        if not user:
            flash("Käyttäjänimi väärin")
            return render_template("login.html")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                flash("Kirjautuminen onnistui")
                session["csrf_token"] = secrets.token_hex(16)
                session["username"] = username
                return redirect("/")
            else:
                flash("Väärä salasana")
                return render_template("login.html")

@app.route("/registeration",methods=["GET", "POST"])
def register():
    if is_user():     
        return redirect("/")
    if request.method == "GET":
        return render_template("register.html")
    if request.method == 'POST':
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        sql = "SELECT username FROM users WHERE LOWER(username)=LOWER(:username)"
        result = db.session.execute(sql, {"username":username})
        exists = result.fetchone()
        if exists != None:
            error = 'Käyttäjänimi on jo olemassa'
            return render_template("register.html", error=error)
        length = len(username)
        if length < 3:
            error = 'Käyttäjänimessa tulee olla vähintään 3 merkkiä'
            return render_template("register.html", error=error)
        if length > 16:
            error = "Käyttäjänimessä saa olla enintään 16 merkkiä"
            return render_template("register.html", error=error)
        if " " in username:
            error = "Käyttäjänimessä ei saa olla välilyöntejä"
            return render_template("register.html", error=error)
        noletters = True
        for i in username:
            if i.isalpha():
                noletters = False
                break
        if noletters:
            error = "Käyttäjänimessä täytyy olla kirjaimia"
            return render_template("register.html", error=error)
        if password1 != password2:
            error = 'Salasanat eivät täsmää'
            return render_template("register.html", error=error)
        length = len(password1)
        if length < 5:
            error = "Salasanan tulee olla vähintään 5 merkkiä pitkä"
            return render_template("register.html", error=error)
        noletters = True
        nocapital = True
        nonumber = True
        for i in password1:
            if noletters or nocapital:
                if i.isalpha():
                    noletters = False
                if i in string.ascii_uppercase:
                    nocapital = False
            if nonumber:
                if str(i) in "0123456789":
                    nonumber = False
        if noletters:
            error = "Salasanassa tulee olla vähintään 1 kirjain"
            return render_template("register.html", error=error)
        if nocapital:
            error = "Salasanassa tulee olla vähintään 1 isokirjain"
            return render_template("register.html", error=error)
        if nonumber:
            error = "Salasanassa tulee olla vähintään 1 numero"
            return render_template("register.html", error=error)
        hash_value = generate_password_hash(password1)
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, '0')"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        flash("Käyttäjä luotu onnistuneesti")
        return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    flash("Kirjauduttu ulos onnistuneesti")
    return redirect("/")
