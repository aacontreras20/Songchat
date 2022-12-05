from flask import Flask, app, render_template, redirect, request, session
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///songchat.db")

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

#load in key
with open("gitignore.txt", "r") as keyfile:
    cid = keyfile.readline().strip()
    secret = keyfile.readline().strip()


client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

name = "Underwater"
try:
    results = sp.search(q='track:' + name, type='track')

    items = results['tracks']['items']

    if len(items) > 0:
        track = items[0]
        url = track['album']['images'][0]['url']

    print(url)

except:
    print("not a song")

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

        '''
        if not len(request.form.get("password")) > 8:
            return apology("password must be greater than 8 characters")
        '''
        
        #check if username is taken
        rows1 = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows1) != 0:
            return apology("username taken")

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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

@app.route('/')
def home():
    return render_template("template.html")


@app.route('/post')
def post():
    return render_template("feed.html")


@app.route('/feed')
def feed():
    return render_template("feed.html")


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()

