import sys, subprocess
# from replit import clear

subprocess.check_call([sys.executable, "-m", "pip", "install", 'discord-oauth2.py'])
# clear()

from flask import Flask, redirect, request
import discordoauth2
import os, json

app = Flask('Discord OAuth2 Example')
client = discordoauth2.Client(id=1208095401094414387, secret=d4rJ2-ql9Zp92-GbdainnyPRrzdwhr6y,
redirect="https://plain-leg-warmers-crab.cyclic.app/oauth2", bot_token=MTIwODA5NTQwMTA5NDQxNDM4Nw.GHZQxY.w378-X2fZztsDafTxHREhH947I4rOCZd8-q2ss

@app.route('/')
def main():
  return redirect("https://discord.com/oauth2/authorize?client_id=1208095401094414387&response_type=code&redirect_uri=https%3A%2F%2Fplain-leg-warmers-crab.cyclic.app%2Fcallback&scope=identify+guilds+guilds.join%20guilds.members.read")

@app.route('/oauth2', methods=["GET"])
def oauth():
    tokenObject = client.exchange_code(request.args.get('code'))
    print("refresh token: "+tokenObject.refresh_token)
    
    identify = tokenObject.fetch_identify()
    connections = tokenObject.fetch_connections()
    guilds = tokenObject.fetch_guilds()
    return f"""<pre style=\"word-wrap: break-word; white-space: pre-wrap;\">
{json.dumps(identify, indent=2)}
</pre>
<br>
<pre style=\"word-wrap: break-word; white-space: pre-wrap;\">
{json.dumps(connections, indent=2)}
</pre>
<br>
<pre style=\"word-wrap: break-word; white-space: pre-wrap;\">
{json.dumps(guilds, indent=2)}
</pre>
<br>
test joining servers!
<form action="/oauth2/guild_join" method="post">
  <input name="nick" placeholder="put a join nickname here" type="text">
  <input name="access" type="hidden" value=" {tokenObject.token}">
  <input type="submit">
</form>
"""

@app.route('/oauth2/guild_join', methods=["POST"])
def oauth_guild_join():
  access = client.from_access_token(request.form["access"])

  access.join_guild(1043078102357651486, nick=request.form["nick"])
  return "", 204

if __name__ == '__main__':
    app.run(debug=True)
