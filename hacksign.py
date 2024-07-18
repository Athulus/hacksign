from flask import Flask, request, url_for, render_template, redirect, flash

import socket

# Constants
COLUMNS = 32
LINES = 4
COLOR_GREEN_BLACK = chr(27) + "[31{"
COLOR_RED_BLACK = chr(27) + "[30{"
COLOR_ORANGE_BLACK = chr(27) + "[29{"
COLOR_BLACK_GREEN = chr(27) + "[63{"
COLOR_BLACK_RED = chr(27) + "[62{"
COLOR_BLACK_ORANGE = chr(27) + "[61{"

# Colors array
colors = [
    COLOR_GREEN_BLACK,
    COLOR_RED_BLACK,
    COLOR_ORANGE_BLACK,
    COLOR_BLACK_GREEN,
    COLOR_BLACK_RED,
    COLOR_BLACK_ORANGE,
]


app = Flask(__name__)

app.config.from_mapping(SECRET_KEY="dev")


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        message = request.form["message"]
        print(message)
        send_to_sign(message=message, message_color=COLOR_GREEN_BLACK)
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
    # Establish socket connection
    host = host  # Replace with the correct host
    port = port  # Replace with the correct port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    # Clear entire screen
    sock.sendall(chr(27).encode() + "[2J".encode())
    # Loop through lines and columns
    for line in range(1, LINES + 1):
        sock.sendall(chr(27).encode() + "[{};1H".format(line).encode())
        color_cycle = iter(colors)
        for column in range(1, COLUMNS + 1):
            try:
                color = next(color_cycle)
            except StopIteration:
                color_cycle = iter(colors)
                color = next(color_cycle)
            sock.sendall(color.encode() + chr(36).encode())
    # Custom message at a specific position
    custom_message = f"{message_color} {message} "
    sock.sendall(
        chr(27).encode()
        + "[2;1H".encode()
        + chr(27).encode()
        + "[0K".encode()
        + custom_message.encode()
    )
    # Close the socket
    sock.close()
