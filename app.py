import os
from flask import Flask, request, redirect, render_template, jsonify, json
from routes.discord_oauth import DiscordOauth
import requests
UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

guild_id = os.getenv('GUILD_ID')
bot_token = os.getenv('BOT_TOKEN')

@app.route('/login', methods=['GET'])
def login():
    return redirect(DiscordOauth.login_url)

@app.route('/upload', methods=['POST'])
def upload():
    # Same cool stuff here.
    print(request.form.get('data'))

    return jsonify(message='success')

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
