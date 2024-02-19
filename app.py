


from flask import Flask, g, render_template, request, redirect, session, url_for, jsonify
from requests_oauthlib import OAuth2Session
import requests


API_ENDPOINT = 'https://discord.com/api/v10'
TOKEN_URL = "https://discord.com/api/oauth2/token"

# https://analogone.pages.dev
OAUTH2_CLIENT_ID = "1208095401094414387" #Your client ID
OAUTH2_CLIENT_SECRET = "d4rJ2-ql9Zp92-GbdainnyPRrzdwhr6y" #Your client secret
OAUTH2_REDIRECT_URI = "https://tough-lingerie-bear.cyclic.app/callback" #Your redirect URL
BOT_TOKEN = "MTIwODA5NTQwMTA5NDQxNDM4Nw.GHZQxY.w378-X2fZztsDafTxHREhH947I4rOCZd8-q2ss" #"Your application token here"
REDIRECT_URL = "https://tough-lingerie-bear.cyclic.app/me"  # Your Oauth redirect URI
GUILD_ID = 1208721793532039209 #The ID of the guild you want them to join
ROLE_IDS = [0] #List of the IDs of the roles you want them to get
AUTORISATION_URL = "me.html" #The obtained URL


API_BASE_URL = 'https://discord.com/api/v10'
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'



app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)


@app.route('/')
def index():
    scope = request.args.get(
        'scope',
        'identify guilds guilds.join')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')

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
    return redirect(REDIRECT_URL)


    
@app.route('/me')
def me():
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
    connections = discord.get(API_BASE_URL + '/users/@me/connections').json()
    return render_template("me.html", user=user, guilds=guilds, connections=connections)


if __name__ == '__main__':
    app.run()
