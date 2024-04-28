import os

from dotenv import load_dotenv
from slack_bolt import App, Ack

# Initializes your app with your bot token and signing secret

from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

from Connect4 import Connect4, Game

load_dotenv()
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


games = {}


@app.command("/startgame")
def start_game(ack: Ack, say, command):
    ack()
    user_id = command['user_id']
    channel_id = command['channel_id']
    if channel_id in games:
        say("A game is already in progress in this channel.")
    else:
        games[channel_id] = Game(player1=user_id)
        say(f"New Connect 4 game started!\n{games[channel_id].__str__()}")


# Make a move
@app.command("/makemove")
def make_move(ack: Ack, say, command):
    ack()
    channel_id = command['channel_id']
    user_id = command['user_id']
    current_game = games.get(channel_id)
    text = command['text']

    if current_game is None:
        say("No active game. Start a new game with /startgame.")
        return

    if user_id != current_game.player1 and current_game.player2 is None:
        current_game.player2 = user_id
        current_game.update_turn()

    # todo add restriction to make sure only the players can make a move
    try:
        col = int(text.strip())
        if channel_id in games:
            valid_move, message = current_game.make_move(col, user_id)
            if valid_move:
                if "wins" in message:
                    if message == "Player A wins!":
                        message = f"Player <@{current_game.player1}> wins!"
                    else:
                        message = f"Player <@{current_game.player2}> wins!"
                    del games[channel_id]  # Remove game if finished
                    say(f'{message}\n{current_game}\nGame over!')
                else:
                    say(f"{current_game}")

            else:
                say(message)
        else:
            say("No active game. Start a new game with /startgame.")
    except ValueError:
        say("Please provide a valid column number (0-6).")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.getenv("PORT", 3000)))
