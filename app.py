from flask import Flask
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
import string

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT M.id, M.name, I.year FROM Movies M LEFT JOIN information I on I.movie_id = M.id ORDER BY M.id DESC limit 10"
    result = db.session.execute(sql)
    movies = result.fetchall()
    return render_template("index.html", movies=movies)

@app.route("/movie/<int:id>")
def movie(id):
    sql = "SELECT M.name, M.id, I.year, I.length FROM Movies M LEFT JOIN information I on I.movie_id = M.id WHERE M.id=:id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()
    sql = "SELECT A.stars, A.user_id, A.review, U.username FROM reviews A, users U WHERE A.movie_id=:id AND A.user_id=U.id"
    result = db.session.execute(sql, {"id":id})
    reviews = result.fetchall()
    sql = "SELECT SUM(stars)/COUNT(*) FROM reviews WHERE movie_id=:id"
    result = db.session.execute(sql, {"id":id})
    all_stars = result.fetchone()
    return render_template("movie.html", id=id, movie=movie, reviews=reviews, all_stars=all_stars)

@app.route("/new_review/<int:id>")
def new_review(id):
    try:
        if session["username"]:
            sql = "SELECT name FROM Movies WHERE id=:id"
            result = db.session.execute(sql, {"id":id})
            movie = result.fetchone()
            username = session['username']
            sql = "SELECT id FROM users WHERE username=:username"
            result = db.session.execute(sql, {"username":username})
            user_id = result.fetchone()[0]
            return render_template("new_review.html", id=id, movie=movie, user_id=user_id)
    except:
        return render_template("new_review.html")

@app.route("/leave_review", methods=["POST"])
def leave_review():
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
    try:
        if session["username"]:
            return redirect("/")
    except:
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
                    session["username"] = username
                    return redirect("/")
                else:
                    flash("Väärä salasana")
                    return render_template("login.html")

@app.route("/registeration",methods=["GET", "POST"])
def register():
    try:
        if session["username"]:
            return redirect("/")
    except:
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
