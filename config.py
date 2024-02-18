from urllib.parse import quote

PORT = 5000
BOT_TOKEN = "MTIwODA5NTQwMTA5NDQxNDM4Nw.GHZQxY.w378-X2fZztsDafTxHREhH947I4rOCZd8-q2ss"
CLIENT_SECRET = "d4rJ2-ql9Zp92-GbdainnyPRrzdwhr6y"
CLIENT_ID = 1208095401094414387  # Enter your bot's client ID
REDIRECT_URI = (
    f"https://tough-lingerie-bear.cyclic.app/callback"  # Your Oauth redirect URI
)
OAUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={quote(REDIRECT_URI)}&response_type=code&scope=identify"
