import hashlib
from BrokenGlass.database import cursor
from flask import render_template, redirect, request, session, url_for
from BrokenGlass import app
from BrokenGlass.decorators import authenticated_resource


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM User WHERE username = %s AND password = %s;", [username, password_hash])
        account = cursor.fetchone()
        if account:
            cursor.execute("UPDATE UserProfile SET LastSignIn = CURDATE() WHERE Username = %s", account[0])
            session["id"] = account[0] + account[1]
            session["username"] = account[0]
            return redirect(url_for("mypage"))
        else:
            error = "ユーザー名またはパスワードが正しくありません。"
    return render_template("login.html", error=error)


@app.route("/logout")
@authenticated_resource
def logout():
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
