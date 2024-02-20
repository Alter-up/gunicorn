from flask import Flask, request, redirect, render_template
from routes.discord_oauth import DiscordOauth
API_ENDPOINT = 'https://discord.com/api/v10'
TOKEN_URL = "https://discord.com/api/oauth2/token"

OAUTH2_CLIENT_ID = "1208095401094414387" #Your client ID
OAUTH2_CLIENT_SECRET = "d4rJ2-ql9Zp92-GbdainnyPRrzdwhr6y" #Your client secret
OAUTH2_REDIRECT_URI = "https://plain-leg-warmers-crab.cyclic.app/callback" #Your redirect URL
BOT_TOKEN = "MTIwODA5NTQwMTA5NDQxNDM4Nw.GHZQxY.w378-X2fZztsDafTxHREhH947I4rOCZd8-q2ss" #"Your application token here"
REDIRECT_URL = "https://plain-leg-warmers-crab.cyclic.app/me"  # Your Oauth redirect URI
GUILD_ID = 1208721793532039209 #The ID of the guild you want them to join
ROLE_IDS = [0] #List of the IDs of the roles you want them to get
AUTORISATION_URL = "" #The obtained URL


app = Flask(__name__)


# Route for index page
# Provides user login capabilities
@app.route('/login', methods=['GET'])
def login():
    return redirect(DiscordOauth.login_url)


# Route for dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    code = request.args.get('code')
    access_token = DiscordOauth.get_access_token(code)

    user_object = DiscordOauth.get_user(access_token)
    user_guild_object = DiscordOauth.get_user_current_guild(access_token)

    id, avatar, username, usertag = user_object.get('id'), user_object.get('avatar'), user_object.get('username'), \
                                    user_object.get('discriminator')


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

    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }

    #Extract the id
    user_object.get('id')

    #URL for adding a user to a guild
    url = f"{API_ENDPOINT}/guilds/{GUILD_ID}/members/{user_id}"

    headers = {
        "Authorization": f"Bot {BOT_TOKEN}"
    }

    response = requests.put(url=url, headers=headers, json=data)

    print(response.text)

    return render_template('dashboard.html', render_user_avatar=f'https://cdn.discordapp.com/avatars/{id}/{avatar}.png',
                           render_username=f'{username}#{usertag}', render_guild=user_guild_object)




if __name__ == '__main__':
    app.run(debug=True)
