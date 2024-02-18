import discordoauth2
from flask import Flask, request

client = discordoauth2.Client(1208095401094414387, secret="d4rJ2-ql9Zp92-GbdainnyPRrzdwhr6y",
redirect="https://tough-lingerie-bear.cyclic.app/oauth2", bot_token="MTIwODA5NTQwMTA5NDQxNDM4Nw.GHZQxY.w378-X2fZztsDafTxHREhH947I4rOCZd8-q2ss")
app = Flask(__name__)

client.update_linked_roles_metadata([
    {
        "type": 2,
        "key": "level",
        "name": "Level",
        "description": "The level the user is on"
    },
    {
        "type": 7,
        "key": "supporter",
        "name": "Supporter",
        "description": "Spent money to help the game"
    }
])

@app.route('/')
def main():
  return redirect(client.generate_uri(scope=["identify", "connections", "guilds", "role_connections.write"]))

@app.route("/oauth2")
def oauth2():
    code = request.args.get("code")

    access = client.exchange_code(code)

    access.update_metadata("Platform Name", "Username",  level=69, supporter=True)

    identify = access.fetch_identify()
    connections = access.fetch_connections()
    guilds = access.fetch_guilds()

    return f"""{identify}<br><br>{connections}<br><br>{guilds}"""

if __name__ == "__main__":
      app.run(debug=True)
