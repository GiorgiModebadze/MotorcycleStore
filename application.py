import os
import base64
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from cachelib.file import FileSystemCache
from werkzeug.security import check_password_hash, generate_password_hash
from io import BytesIO
from PIL import Image
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


@app.route("/", methods=["GET", "POST"])
def index():
    searched = False
    advertisments = db.execute(
        "Select advertisment.id as uid, * From advertisment left join users on advertisment.user_id = users.id where active = 1 order by created_at desc")

    if request.method == "POST" and not request.form.get('clearsearch'):
        searched = True
        search_make = request.form['make']
        advertisments = db.execute(
            "Select advertisment.id as uid, * From advertisment left join users on advertisment.user_id = users.id where active = 1 and make = :make order by created_at desc", make=search_make)

    search_makes = []
    for picture in advertisments:
        p_data = Image.open(BytesIO(picture['picture']))
        p_data.save(f"static/images/{picture['picture_name']}", "JPEG", quality=80,
                    optimize=True, progressive=True)

        search_makes.append(picture['make'])
    search_makes = list(set(search_makes))
    return render_template("index.html", advertisments=advertisments, search_makes=search_makes, searched=searched)

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
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')

        if len(password) < 6:
            return apology("password must be at least 6 letters long", 403)

        if password != confirmation:
            return apology("confirmation and password does not match", 403)

        hashed_pass = generate_password_hash(password)

        db.execute("INSERT INTO Users (username, hash, phone_number, email ) VALUES (:username, :hashed_pass, :phone_number, :email)",
                   username=username, hashed_pass=hashed_pass, phone_number=phone_number, email=email)

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

    if request.method == "POST":
        pic = request.files['picture']
        print(pic.filename)
        db.execute('''INSERT INTO advertisment (user_id, condition, make,model,category,price,milage,hp,color,picture, picture_name,  description,active) VALUES
        (:user_id, :condition, :make, :model, :category, :price, :milage, :hp, :color, :picture, :picture_name, :description , 1);''',
                   user_id=session['user_id'],
                   condition=request.form.get('condition'),
                   make=request.form.get('make'),
                   model=request.form.get('model'),
                   category=request.form.get('category'),
                   price=request.form.get('price'),
                   milage=request.form.get('milage'),
                   hp=request.form.get('hp'),
                   color=request.form.get('color'),
                   picture=pic.read(),
                   picture_name=pic.filename,
                   description=request.form.get('description')
                   )

    conditions = db.execute("select id, condition_name from condition;")
    make_dict = db.execute("select id, make from make order by make;")

    model_dict = db.execute(
        "select model, make from model inner join make on model.make_id = make.id order by make, model")
    models = [model['model'] + ":" +
              model['make'] for model in model_dict]

    category_dict = db.execute("select id, category from category")
    colors = db.execute("select id, color from color")
    return render_template("sell.html", conditions=conditions, makes=make_dict, models=models, categories=category_dict, colors=colors)


@app.route("/my_advertisments", methods=["GET", "POST"])
@login_required
def my_advertisments():
    if request.method == "POST":
        db.execute("Update advertisment set active = 0 where id = :uid",
                   uid=int(request.form.get('adv_id')))

    advertisments = db.execute(
        "Select advertisment.id as uid, * From advertisment left join users on advertisment.user_id = users.id where users.id = :user_id and active = 1 order by created_at desc", user_id=session['user_id'])
    for picture in advertisments:
        p_data = Image.open(BytesIO(picture['picture']))
        p_data.save(f"static/images/{picture['picture_name']}", "JPEG", quality=80,
                    optimize=True, progressive=True)

    return render_template("my_advertisments.html", advertisments=advertisments)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allows User To change Password"""

    if request.method == "POST":

        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if len(password) < 6:
            return apology("password must be at least 6 letters long", 403)

        if password != confirmation:
            return apology("confirmation and password does not match", 403)

        hashed_pass = generate_password_hash(password)

        db.execute("Update Users set hash = :hashed_pass where id = :user_id;",
                   user_id=session["user_id"], hashed_pass=hashed_pass)

        return redirect("/")

    # Redirect user to login form
    return render_template("change_password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
