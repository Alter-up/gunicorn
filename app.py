from flask import Flask, g, render_template, request, redirect, session, url_for, jsonify
from requests_oauthlib import OAuth2Session
import requests


API_ENDPOINT = 'https://discord.com/api/v10'
TOKEN_URL = "https://discord.com/api/oauth2/token"

# https://analogone.pages.dev
OAUTH2_CLIENT_ID = "1208095401094414387" #Your client ID
OAUTH2_CLIENT_SECRET = "d4rJ2-ql9Zp92-GbdainnyPRrzdwhr6y" #Your client secret
OAUTH2_REDIRECT_URI = "https://plain-leg-warmers-crab.cyclic.app/callback" #Your redirect URL
BOT_TOKEN = "MTIwODA5NTQwMTA5NDQxNDM4Nw.GHZQxY.w378-X2fZztsDafTxHREhH947I4rOCZd8-q2ss" #"Your application token here"
REDIRECT_URL = "https://plain-leg-warmers-crab.cyclic.app"  # Your Oauth redirect URI
GUILD_ID = 1208721793532039209 #The ID of the guild you want them to join
ROLE_IDS = [0] #List of the IDs of the roles you want them to get
AUTORISATION_URL = "" #The obtained URL



app = Flask(__name__)

@app.route('/')
def main():
    return redirect(AUTORISATION_URL)


@app.route('/callback')
def callback():
    print("flag")
    if request.values.get('error'):
        return request.values['error']

    args = request.args
    code = args.get('code')

    data = {
        'client_id': OAUTH2_CLIENT_ID,
        'client_secret': OAUTH2_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': OAUTH2_REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post("https://discord.com/api/v10/oauth2/token", data=data, headers=headers)
    r.raise_for_status()

    #Get the acces token
    access_token = r.json()["access_token"]

    #Get info of the user, to get the id
    url = f"{API_ENDPOINT}/users/@me"

    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }

    #This will contain the information
    response = requests.get(url=url, headers=headers)

    print(response.json())

    #Extract the id
    user_id = response.json()["id"]

    #URL for adding a user to a guild
    url = f"{API_ENDPOINT}/guilds/{GUILD_ID}/members/{user_id}"

    headers = {
        "Authorization": f"Bot {BOT_TOKEN}"
    }

    #These lines specifies the data given. Acces_token is mandatory, roles is an array of role ids the user will start with.
    data = {
        "access_token": access_token,
        "roles": ROLE_IDS
    }

    #Put the request
    response = requests.put(url=url, headers=headers, json=data)

    print(response.text)
    return render_template("index.html", user=username, guilds=guilds, connections=connections)


if __name__ == '__main__':
    app.run()
