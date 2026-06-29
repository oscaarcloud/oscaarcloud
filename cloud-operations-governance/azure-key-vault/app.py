import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    conn = os.environ.get("DB_CONNECTION_STRING", "NOT_FOUND")

    if conn == "NOT_FOUND":
        return "DB_CONNECTION_STRING environment variable not found."

    masked = conn[:35] + "..." if len(conn) > 35 else conn
    return f"Banking app secret loaded successfully: {masked}"