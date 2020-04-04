import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from cachelib.file import FileSystemCache
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.route("/")
# @login_required
def index():
    return render_template("index.html")

# Used from Harvards CS50 Implementation
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        # check if the username is empty
        if not username:
            return apology("must provide valid username", 403)

        # Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        if len(rows) > 0:
            return apology("username already exists, please try another one", 403)

        # Check if password is less than 6 char long
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if len(password) < 6:
            return apology("password must be at least 6 letters long", 403)

        if password != confirmation:
            return apology("confirmation and password does not match", 403)

        hashed_pass = generate_password_hash(password)

        db.execute("INSERT INTO Users (username, hash) VALUES (:username, :hashed_pass)",
                   username=username, hashed_pass=hashed_pass)

        user_id = db.execute("select id from users where username = :username",
                             username=username)

        session["user_id"] = user_id[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
def sell():

    conditions = db.execute("select condition_name from condition;")
    make_dict = db.execute("select make from make;")
    makes = [make['make'] for make in make_dict]
    makes.sort()
    return render_template("sell.html", conditions=conditions, makes=makes)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
