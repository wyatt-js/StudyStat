from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    connect = sqlite3.connect("data.db")
    cursor = connect.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT,
            time_total INTEGER
        )
    """)
    connect.commit()
    connect.close()

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.get_json()
    client_id = data.get("client_id")
    time_total = data.get("data")
    connect = sqlite3.connect("data.db")
    cursor = connect.cursor()
    cursor.execute("INSERT INTO logs (client_id, time_total) VALUES (?, ?)", (client_id, time_total))
    connect.commit()
    connect.close()
    return jsonify({"status": "success", "message": "Data received"}), 200