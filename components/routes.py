from app import app
from flask import redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import repositories.users as u_repository
import repositories.movies as m_repository
import string, secrets

@app.route("/")
def index():
    movies = m_repository.first_page()
    admin = u_repository.is_admin()
    return render_template("index.html", movies=movies, admin=admin, req=True)

@app.route("/movie/<int:id>")
def movie(id):
    movie = m_repository.movie(id)
    platforms = m_repository.platforms(id)
    admin = u_repository.is_admin()
    if admin:
        all_platforms = m_repository.all_platforms()
        return render_template("movie.html", id=id, movie=movie, platforms=platforms, all_platforms=all_platforms, admin=admin, req=True)
    return render_template("movie.html", id=id, movie=movie, platforms=platforms, admin=admin, req=True)

@app.route("/add_movie_platform", methods=["POST"])
def add_movie_platform():
    if u_repository.is_admin():
        platform_id = request.form.get("platform") 
        movie_id = request.form["movie_id"]
        if platform_id and movie_id:
            m_repository.add_movie_platform(platform_id, movie_id)
            return redirect("/movie/"+movie_id)
        flash("Jotain meni pieleen")
    return redirect("/")

@app.route("/delete_movie_platform", methods=["POST"])
def delete_movie_platform():
    if u_repository.is_admin():
        platform_id = request.form["platform_id"]
        movie_id = request.form["movie_id"]
        m_repository.delete_movie_platform(movie_id, platform_id)
        return redirect("/movie/"+movie_id)
    return redirect("/")

@app.route("/new_platform", methods=["GET"])
def new_platform():
    if u_repository.is_admin():
        return render_template("platform.html")
    return redirect("/")

@app.route("/add_platform", methods=["POST"])
def add_platform():
    if not u_repository.is_admin():
        return redirect("/")
    name = request.form["platform_name"]
    link = request.form["platform_link"]
    if name and link:
        m_repository.add_platform(name, link)
        flash("Alusta lisätty onnistuneesti")
    return redirect("/")

@app.route("/search_result", methods=["GET"])
def search_result():
    search_by = request.args["search_by"]
    query = request.args["query"]
    if search_by == "name":
        movies = m_repository.search_movies_name(query)
        return render_template("search_result.html", movies=movies, req=True)
    if search_by == "genre":
        movies = m_repository.search_movies_genre(query)
        return render_template("search_result.html", movies=movies, req=True)

@app.route("/movie_request", methods=["GET"])
def movie_request():
    return render_template("movie_request.html", name="", year="")

@app.route("/leave_request", methods=["POST"])
def leave_request():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    movie_name = request.form["movie_name"]
    movie_year = request.form["movie_year"]
    movie_name, movie_year, success = m_repository.leave_request(movie_name, movie_year)
    if success:
        flash("Pyyntö jätetty onnistuneesti")
        return redirect("/")
    flash("Vuosiluvun tulee olla numero")
    return render_template("movie_request.html", name=movie_name, year=movie_year)

@app.route("/all_requests")
def requests():
    if not u_repository.is_admin():
        return redirect("/")
    movies = m_repository.get_requests()
    return render_template("requests.html", movies=movies)

@app.route("/new_movie<int:id>", methods=["GET"])
def new_movie(id):
    if not u_repository.is_admin():
        return redirect("/")
    movie = m_repository.get_request(id)
    return render_template("new_movie.html", movie=movie, id=id)

@app.route("/add_movie", methods=["POST"])
def add_movie():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if not u_repository.is_admin():
        flash("Et ole ylläpitäjä")
        return redirect("/")
    movie_name = request.form["name"]
    movie_year = request.form["year"]
    movie_length = request.form["length"]
    movie_genre = request.form["genre"]
    description = request.form["description"]
    id = request.form["id"]
    movie_id, movie_name = m_repository.add_movie(movie_name, movie_year, movie_length, movie_genre)
    m_repository.add_description(movie_id, description) 
    m_repository.delete_request(id, movie_name)
    flash("Elokuva lisätty onnistuneesti!")
    return redirect("/all_requests")

@app.route("/delete_movie", methods=["POST"])
def delete_movie():
    if not u_repository.is_admin():
        return redirect("/")
    movie_id = request.form["movie_id"]
    m_repository.delete_all_movie_platforms(movie_id)
    m_repository.delete_movie_reviews(movie_id)
    m_repository.delete_description(movie_id)
    m_repository.delete_movie(movie_id)
    flash("Elokuva poistettu!")
    return redirect("/")

@app.route("/new_review/<int:id>")
def new_review(id):
    if u_repository.is_user():
        movie = m_repository.movie(id)
        username = session['username']
        user_id = u_repository.find_user_id(username)
        review=""
        return render_template("new_review.html", id=id, movie=movie, user_id=user_id, review=review, req=True)
    return render_template("new_review.html", req=True)

@app.route("/leave_review", methods=["POST"])
def leave_review():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    movie_id = request.form["id"]
    if "stars" not in request.form:
        flash("Anna elokuvalle arvostelu")
        movie = m_repository.movie(movie_id)
        username = session['username']
        user_id = u_repository.find_user_id(username)
        review = request.form["review"]
        return render_template("new_review.html", id=movie_id, movie=movie, user_id=user_id, review=review, req=True)
    stars = request.form["stars"]
    review = request.form["review"]
    user_id = request.form["user_id"]
    m_repository.leave_review(movie_id, stars, review, user_id)
    return redirect("/movie/" + str(movie_id))

@app.route("/delete_review/<int:id>")
def delete_review(id):
    movie_id = m_repository.delete_review(id)
    return redirect("/movie/"+str(movie_id))

@app.route("/login",methods=["GET", "POST"])
def login():
    if u_repository.is_user():
        return redirect("/")
    if request.method == 'GET':
        return render_template("login.html", username="", password="")
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = u_repository.get_user(username)
        if not user:
            flash("Käyttäjää ei ole olemassa")
            return render_template("login.html", username=username, password=password)
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                flash("Kirjauduttu sisään onnistuneesti")
                session["csrf_token"] = secrets.token_hex(16)
                session["username"] = username
                return redirect("/")
            else:
                flash("Väärä salasana")
                return render_template("login.html", username=username, password=password)

@app.route("/registeration",methods=["GET", "POST"])
def register():
    if u_repository.is_user():     
        return redirect("/")
    if request.method == "GET":
        return render_template("register.html", username="", password1="", password2="")
    if request.method == 'POST':
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        exists = u_repository.get_user(username)
        if exists != None:
            error = 'Käyttäjänimi on jo olemassa'
            return render_template("register.html", error=error, username=username, password1=password1, password2=password2)
        error = u_repository.check_username(username)
        if error:
            return render_template("register.html", error=error, username=username, password1=password1, password2=password2)
        if password1 != password2:
            error = 'Salasanat eivät täsmää'
            return render_template("register.html", error=error, username=username, password1=password1, password2=password2)
        error = u_repository.check_password(password1)
        if error:
            return render_template("register.html", error=error, username=username, password1=password1, password2=password2)
        hash_value = generate_password_hash(password1)
        u_repository.add_user(username, hash_value)
        flash("Käyttäjä luotu onnistuneesti")
        return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    flash("Kirjauduttu ulos onnistuneesti")
    return redirect("/")
