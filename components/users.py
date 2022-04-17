from database_connection import db

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
        if a == '1':
            admin = True
    return admin

