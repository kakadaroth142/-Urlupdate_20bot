#!/usr/bin/env python3
import threading
from flask import Flask
from bot import run_bot

app = Flask('app')

@app.route('/')
def hello_world():
    return 'Bot is running!'

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    run_bot()
