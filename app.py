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
    result = db.session.execute("SELECT id, name FROM Movies")
    movies = result.fetchall()
    return render_template("index.html", count=len(movies), movies=movies)

@app.route("/movie/<int:id>")
def movie(id):
    sql = "SELECT name FROM Movies WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    movie = result.fetchone()[0]
    sql = ("SELECT year, length FROM information WHERE movie_id=:id")
    result = db.session.execute(sql, {"id":id})
    information = result.fetchone()
    return render_template("movie.html", id=id, movie=movie, information=information)

@app.route("/login",methods=["GET", "POST"])
def login():
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
    return redirect("/")
