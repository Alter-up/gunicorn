import os
from flask import Flask, request, redirect, render_template
from routes.discord_oauth import DiscordOauth
import requests

app = Flask(__name__)

guild_id = os.getenv('GUILD_ID')
bot_token = os.getenv('BOT_TOKEN')

@app.route('/login', methods=['GET'])
def login():
    return redirect(DiscordOauth.login_url)


# Route for dashboard
@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    code = request.args.get('code')
    access_token = DiscordOauth.get_access_token(code)

    user_object = DiscordOauth.get_user(access_token)
    user_guild_object = DiscordOauth.get_user_current_guild(access_token)

    id, avatar, username, usertag = user_object.get('id'), user_object.get('avatar'), user_object.get('username'), \
                                    user_object.get('discriminator')

    url = f'https://discordapp.com/api/v8/guilds/{guild_id}/members/{id}'
    headers = {
        'Authorization': f'Bot {bot_token}'
    }

    data = {
        "access_token": access_token
    }
    response = requests.put(url, headers=headers, json=data)

   
    return render_template('dashboard.html', render_user_avatar=f'https://cdn.discordapp.com/avatars/{id}/{avatar}.png',
                           render_username=f'{username}#{usertag}', render_guild=user_guild_object)




if __name__ == '__main__':
    app.run(debug=True)
@app.route('/upload', methods=['POST'])
def upload():
    # Same cool stuff here.
    print(request.form.get('data'))

    return jsonify(message='success')
