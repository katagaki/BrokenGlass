from datetime import timedelta

from flask import Flask

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = "something unique and secret 37591"
app.permanent_session_lifetime = timedelta(minutes=10)

import BrokenGlass.main
import BrokenGlass.auth
import BrokenGlass.matome
