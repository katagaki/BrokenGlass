from BrokenGlass.database import cursor
from BrokenGlass.decorators import authenticated_resource
from flask import render_template, redirect, request, session, url_for

from BrokenGlass import app


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/mypage")
@authenticated_resource
def mypage():
    username = session["username"]
    cursor.execute("SELECT Name, LastSignIn FROM UserProfile WHERE username = %s;", [username])
    fetched_user_profile = cursor.fetchone()
    user_profile = {
        "name": fetched_user_profile[0],
        "lastSignIn": fetched_user_profile[1]
    }
    return render_template(
        "mypage.html",
        profile=user_profile
    )

