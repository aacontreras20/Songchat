# Songchat
YouTube Link to Presentation: https://youtu.be/8H9zXQEuujg

To successfully compile, configure, and use our project, we suggest that the staff opens it up on VSCode where they have flask, python, and all necessary languages installed with the cs50 library (as done in our code since we worked on our local VSCode). We implemented spotipy in this project, to pull the song title and image for the posts in the feed. If a user were to make posts on one account then log out and log in with another account, they would see the posts from the prior account still on their feed. When the user first visits our Songchat site, we suggest they first click on the Register tab on the top right, which will take them to the register HTML page. Here for optimal usage, the user should type in a username they haven't already used to make an account, as well as their Spotify Username, and a password that matches what they enter in the password confirmation text field.

If successfully registered, the user will be redirected to the login page, where they should enter the username and password for the account they wish to sign into. If they successfully login by properly spelling their username and password and ensuring that the account exists by having registered, they will be redirected to the homepage, which will have a fadeIn effect to the Songchat title. From the homepage, the user should head to the post tab (post.html) via the navbar and post about any song they'd like. Once the user clicks the "post" button, the page will redirect them to the feed page, on which they can see all posts they've made in a list. The user can also head over to the profile page, which will show the username, Spotify username, and posts made by the user's current logged in account. If the user would like to log out of their account, they can simply click the log out tab on the top right of the navbar while they're logged in, which will log them out of the site and redirect them to the login page.

** For context, while we included the karma feature in the songchat.db file and made buttons to upvote and downvote, as well as the karma score displayed on the site of each post, we were unable to fully implement the feature due to time constraints, so we instead implemented the profile page and Spotify API successfully as mentioned in our initial Final Project Proposal **


Directions on how to configure app:

1. Clone this repository.

`$ git clone https://github.com/aacontreras20/Songchat.git`

2. Create a new virtual environment. Learn more about those [here](https://docs.python.org/3/tutorial/venv.html "Virtual Environments in Python").

`$ python3 -m venv ~/<your_env_name>`<br>
`$ source your_env_name/bin/activate`

3. Cd into songchat
`$ (your_env_name) cd songchat`

4. Install project dependencies.

`$ (your_env_name) pip3 install -r requirements.txt`

5. Run the app.

`$ (your_env_name) python3 app/__init__.py`


