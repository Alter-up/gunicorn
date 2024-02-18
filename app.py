from flask import Flask, render_template, request, redirect, session
from zenora import APIClient

from .config import BOT_TOKEN, CLIENT_SECRET, OAUTH_URL, REDIRECT_URI

app = Flask(__name__)
client = APIClient(BOT_TOKEN, client_secret=CLIENT_SECRET)

app.config["SECRET_KEY"] = "mysecret"


@app.route("/")
def home():
    access_token = session.get("access_token")

    if not access_token:
        return render_template("index.html")

    bearer_client = APIClient(access_token, bearer=True)
    current_user = bearer_client.users.get_current_user()

    return render_template("index.html", user=current_user)


@app.route("/login")
def login():
    return redirect(OAUTH_URL)


@app.route("/logout")
def logout():
    session.pop("access_token")
    return redirect("/")


@app.route("/oauth/callback")
def oauth_callback():
    code = request.args["code"]
    access_token = client.oauth.get_access_token(
        code, redirect_uri=REDIRECT_URI
    ).access_token
    session["access_token"] = access_token

    return redirect("/")
