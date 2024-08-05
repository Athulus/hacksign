from flask import Flask, request, url_for, render_template, redirect, flash

import socket

# Constants
COLUMNS = 32
LINES = 4
ESC = chr(27)
COLOR_GREEN_BLACK = ESC + "[31{"
COLOR_RED_BLACK = ESC + "[30{"
COLOR_ORANGE_BLACK = ESC + "[29{"
COLOR_BLACK_GREEN = ESC + "[63{"
COLOR_BLACK_RED = ESC + "[62{"
COLOR_BLACK_ORANGE = ESC + "[61{"

# Colors array
colors = {
    "gb": COLOR_GREEN_BLACK,
    "rb": COLOR_RED_BLACK,
    "ob": COLOR_ORANGE_BLACK,
    "bg": COLOR_BLACK_GREEN,
    "br": COLOR_BLACK_RED,
    "bo": COLOR_BLACK_ORANGE,
}


app = Flask(__name__)

app.config.from_mapping(SECRET_KEY="dev")


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        message = request.form["message"]
        color = colors[request.form["color"]]
        print(message)
        send_to_sign(message=message, message_color=color)
        flash(f"'{message}' sent to the sign")
        return redirect(url_for("main"))
    return render_template("hacksign.html")


@app.route("/test/<message>")
def test_sign(message: str):
    send_to_sign(message)

    return message


def send_to_sign(
    message, message_color=COLOR_BLACK_GREEN, host="10.200.200.98", port=23
):
    """
    this will establish a connection to the sign, clear the screen, and send the provided message
    starting at the top left of the screen

    the default host and port are what were hardcoded into the sign when this app was made. change them if nessecary
    """
    # Establish socket connection
    host = host
    port = port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    # Clear entire screen
    sock.sendall(ESC.encode() + "[2J".encode())
    # Custom message at a specific position
    custom_message = f"{message_color}{message} "
    sock.sendall(ESC.encode() + "[;H".encode() + custom_message.encode())
    # Close the socket
    sock.close()
