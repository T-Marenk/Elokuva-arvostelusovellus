from database_connection import db
from flask import session
import string

def is_user():
    user = False
    try:
        if session["username"]:
            user = True
    except:
        pass
    return user

def is_admin():
    admin = False
    if is_user():
        sql = "SELECT admin FROM users WHERE username=:username"
        username = session["username"]
        result = db.session.execute(sql, {"username":username})
        a = result.fetchone()[0]
        if a:
            admin = True
    return admin

def find_user_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    print(user_id)
    return user_id

def get_user(username):
    sql = "SELECT id, password FROM users WHERE LOWER(username)=LOWER(:username)"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user

def check_username(username):
    error = check_length(username)
    if error:
        return error
    if " " in username:
        return "Käyttäjänimessä ei saa olla välilyöntejä"
    error = check_letters(username)
    if check_letters(username):
        return "Käyttäjänimessä täytyy olla ainakin yksi kirjain"
    

def check_length(username):
    length = len(username)
    error = None
    if length < 3:
        error = "Käyttäjänimessä tulee olla vähintään 3 merkkiä"
    elif length > 16:
        error = "Käyttäjänimessä saa olla enintään 16 merkkiä"
    return error if error else None

def check_letters(username):
    for i in username:
        if i.isalpha():
            return False
    return True

def check_password(password):
    if check_length_p(password):
        return "Salasanan tulee olla vähintään 5 merkkiä pitkä"
    elif check_password_letter(password):
        return "Salasanassa tulee olla vähintään 1 kirjain"
    elif check_password_capital(password):
        return "Salasanassa tulee olla iso kirjain"
    elif check_password_number(password):
        return "Salasanassa tulee olla numero"

def check_length_p(password):
    length = len(password)
    if length < 5:
        return True

def check_password_letter(password):
    for i in password:
        if i.isalpha():
            return False
    return True

def check_password_capital(password):
    for i in password:
        if i in string.ascii_uppercase:
            return False
    return True

def check_password_number(password):
    for i in password:
        if str(i) in "0123456789":
            return False
    return True

def add_user(username, password):
    sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, '0')"
    db.session.execute(sql, {"username":username, "password":password})
    db.session.commit()
