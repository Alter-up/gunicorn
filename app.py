from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc
import os


API_ENDPOINT = 'https://discord.com/api/v10'
TOKEN_URL = "https://discord.com/api/oauth2/token"

# https://analogone.pages.dev
OAUTH2_CLIENT_ID = "1208095401094414387" #Your client ID
OAUTH2_CLIENT_SECRET = "d4rJ2-ql9Zp92-GbdainnyPRrzdwhr6y" #Your client secret
OAUTH2_REDIRECT_URI = "https://plain-leg-warmers-crab.cyclic.app/callback" #Your redirect URL
BOT_TOKEN = "MTIwODA5NTQwMTA5NDQxNDM4Nw.GHZQxY.w378-X2fZztsDafTxHREhH947I4rOCZd8-q2ss" #"Your application token here"
REDIRECT_URL = "https://plain-leg-warmers-crab.cyclic.app/me"  # Your Oauth redirect URI
GUILD_ID = 1208721793532039209 #The ID of the guild you want them to join
ROLE_IDS = [0] #List of the IDs of the roles you want them to get
AUTORISATION_URL = "" #The obtained URL

app.config["DISCORD_CLIENT_ID"] = 1208095401094414387  # Discord client ID.
app.config[
    "DISCORD_CLIENT_SECRET"
] = "d4rJ2-ql9Zp92-GbdainnyPRrzdwhr6y"  # Discord client secret.
app.config[
    "DISCORD_REDIRECT_URI"
] = "https://plain-leg-warmers-crab.cyclic.app/callback"  # URL to your callback endpoint.

app = Quart(__name__)
ipc_client = ipc.Client(
    secret_key="this_is_token"
) 

discord = DiscordOAuth2Session(app)


@app.route("/")
async def home():
    return await render_template("index.html", authorized=await discord.authorized)


@app.route("/login")
async def login():
    return await discord.create_session()


@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except Exception:
        pass

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
async def dashboard():
    guild_count = await ipc_client.request("get_guild_count")
    guild_ids = await ipc_client.request("get_guild_ids")
    user = await discord.fetch_user()

    try:
        user_guilds = await discord.fetch_guilds()
    except:
        return redirect(url_for("login"))

    same_guilds = []

    for guild in user_guilds:
        if guild.id in guild_ids:
            same_guilds.append(guild)

    return await render_template(
        "dashboard.html", guild_count=guild_count, matching=same_guilds, user=user
    )


if __name__ == "__main__":
    app.run(debug=True)
