import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///user.db")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation password was submitted
        if not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        # Ensure confirmation password matches password
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords must match", 400)

        # Ensure spotify username was submitted
        if not request.form.get("spotifyuser"):
            return apology("must provide Spotify username", 400)

        if not len(request.form.get("password")) > 8:
            return apology("password must be greater than 8 characters")

        #rows1 = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        #if len(rows1) != 0:
        #    return apology("username taken")

        user = request.form.get("username")
        hashpw = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        spotify = request.form.get("spotifyuser")

        try:
            db.execute("INSERT INTO users (username, hash, spotify) VALUES (?, ?, ?)", user, hashpw, spotify)
            return redirect("/")
        except:
            return apology("username taken", 200)
    else:
        return render_template("register.html")
