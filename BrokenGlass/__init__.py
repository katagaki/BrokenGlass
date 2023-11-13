from flask import Flask

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = "something unique and secret 37591"

import BrokenGlass.main
