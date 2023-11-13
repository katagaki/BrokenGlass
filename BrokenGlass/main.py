import hashlib

from flask import render_template, redirect, request, session, url_for
import pymysql

from BrokenGlass import app

conn = pymysql.connect(host='localhost', port=3306, user='root', password='P@ssw0rd!', db='broken_glass')

def initDB():
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User (
            Username VARCHAR(255) PRIMARY KEY NOT NULL,
            Password TEXT NOT NULL
        );
    """)

    adminPassword = hashlib.sha256(b"password").hexdigest()
    justinPassword = hashlib.sha256(b"rosebud2").hexdigest()

    cursor.execute("INSERT IGNORE INTO User VALUES (%s, %s);", ["admin", adminPassword])
    cursor.execute("INSERT IGNORE INTO User VALUES (%s, %s);", ["justin", justinPassword])

    conn.commit()

initDB()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        passwordHash = hashlib.sha256(password.encode()).hexdigest()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User WHERE username = %s AND password = %s;", [username, passwordHash])
        account = cursor.fetchone()
        if account:
            session["id"] = account[0] + account[1]
            session["username"] = account[0]
            return redirect(url_for('mypage'))
        else:
            error = "ユーザー名またはパスワードが正しくありません。"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/mypage")
def mypage():
    if "id" in session:
        return render_template("mypage.html")
    else:
        return redirect(url_for('login'))