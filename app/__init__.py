from flask import Flask, app, render_template, redirect, request, session
from cs50 import SQL
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

#load in key
with open("gitignore.txt", "r") as keyfile:
    cid = keyfile.readline().strip()
    secret = keyfile.readline().strip()

db = SQL("sqlite:///songchat.db")


client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



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

        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        spotify = request.form.get("spotifyuser")

        db.execute("INSERT INTO users (username, spotify, hash) VALUES(?,?, ?)", username, spotify ,hash)

        return redirect("/")
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
        print(session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/')
def home():
    return render_template("template.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/post', methods=["GET", "POST"])
def post():
    if request.method == "POST":
        song = request.form.get("song")
        content = request.form.get("content")

        try:
            results = sp.search(q='track:' + song, type='track')
            items = results['tracks']['items']
            if len(items) > 0:
                track = items[0]
                name = track['name']
        except:
            return apology("not a valid song", 403)

        db.execute("INSERT INTO posts (user_id, song, content) VALUES(?,?,?)", session["user_id"], name , content)

        return redirect("/")
    else:
        return render_template("post.html")


@app.route('/feed')
def feed():
    #generates sorted feed of posts 
    #Next steps: Make it so that not all the posts show up/load in the data beforehand
    
    rows = db.execute("SELECT * FROM posts ORDER BY post_karma")

    for row in rows:

        results = sp.search(q='track:' + row["song"], type='track')

        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            url = track['album']['images'][0]['url']

        row["image"] = url
        
    print(rows)
    

    return render_template("feed.html", rows = rows)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
