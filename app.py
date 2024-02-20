from flask import Flask, request, redirect, render_template
from routes.discord_oauth import DiscordOauth

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


    return render_template('dashboard.html', render_user_avatar=f'https://cdn.discordapp.com/avatars/{id}/{avatar}.png',
                           render_username=f'{username}#{usertag}', render_guild=user_guild_object)


if __name__ == '__main__':
    app.run(debug=True)
