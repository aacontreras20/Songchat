from flask import Flask, app, render_template, redirect, request
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

#load in key
with open("gitignore.txt", "r") as keyfile:
    cid = keyfile.readline()
    secret = keyfile.readline()


client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)






@app.route('/')
def home():
    #song = sp.search(q = "hello", type = "track")
    

    name = 'Radiohead'

    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']

    if len(items) > 0:
        artist = items[0]
        url = artist['name'], artist['images'][0]['url']

    return render_template("template.html", url = url)



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()