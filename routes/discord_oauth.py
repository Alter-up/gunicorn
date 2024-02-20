import os
import requests
from dotenv import load_dotenv
BOT_TOKEN = "MTIwODA5NTQwMTA5NDQxNDM4Nw.GHZQxY.w378-X2fZztsDafTxHREhH947I4rOCZd8-q2ss"
API_ENDPOINT = "https://discord.com/api/v6"
GUILD_ID = 1208721793532039209 #The ID of the guild you want them to join
REDIRECT_URL = "https://plain-leg-warmers-crab.cyclic.app/dashboard"
load_dotenv()


class DiscordOauth:
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = 'https://plain-leg-warmers-crab.cyclic.app/dashboard'
    scope = 'identify%20guilds'
    login_url = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}'
    token_url = 'https://discord.com/api/oauth2/token'
    api_endpoint = 'https://discord.com/api/v6'

    # Get access token
    @staticmethod
    def get_access_token(code):
        access_token_url = DiscordOauth.token_url

        access_token = requests.post(
            access_token_url,
            data={
                'client_id': DiscordOauth.client_id,
                'client_secret': DiscordOauth.client_secret,
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': DiscordOauth.redirect_uri,
                'scope': DiscordOauth.scope

            }
        ).json()

        return access_token.get('access_token')

    # Get user
    @staticmethod
    def get_user(access_token):
        user_object = requests.get(
            url=f'{DiscordOauth.api_endpoint}/users/@me',
            headers={'Authorization': 'Bearer %s' % access_token}
        ).json()

        return user_object

    # Get user current guild
    @staticmethod
    def get_user_current_guild(access_token):
        user_guild_object = requests.get(
            url=f'{DiscordOauth.api_endpoint}/users/@me/guilds',
            headers={'Authorization': 'Bearer %s' % access_token}
        ).json()

        return user_guild_object

@staticmethod
def dashboard():
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

    response = requests.put(url=url, headers=headers, json=data)

    print(response.text)

