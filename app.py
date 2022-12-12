from flask import Flask
from flask.templating import render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "GOOGOOGAGA"
debug = DebugToolbarExtension(app)

@app.route("/")
def first_route():
    return render_template("base.html")