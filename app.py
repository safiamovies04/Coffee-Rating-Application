from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Create Database and Table
def init_db():
    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            votes INTEGER
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM coffee")
    count = cursor.fetchone()[0]

    if count == 0:
        coffees = [
            ("Espresso", 0),
            ("Cappuccino", 0),
            ("Latte", 0),
            ("Mocha", 0),
            ("Americano", 0)
        ]
        cursor.executemany(
            "INSERT INTO coffee (name, votes) VALUES (?, ?)",
            coffees
        )

    conn.commit()
    conn.close()


# Initialize database
init_db()


@app.route("/")
def home():

    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    # Get all coffee items
    cursor.execute("SELECT * FROM coffee")
    coffees = cursor.fetchall()

    # Get most popular coffee
    cursor.execute("""
        SELECT name, votes
        FROM coffee
        ORDER BY votes DESC
        LIMIT 1
    """)
    top_coffee = cursor.fetchone()

    conn.close()

    return render_template(
        "index.html",
        coffees=coffees,
        top_coffee=top_coffee
    )


@app.route("/vote", methods=["POST"])
def vote():

    data = request.get_json()
    coffee_id = data["id"]

    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    # Increase vote
    cursor.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id=?",
        (coffee_id,)
    )

    conn.commit()

    # Get updated votes
    cursor.execute(
        "SELECT votes FROM coffee WHERE id=?",
        (coffee_id,)
    )

    votes = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "votes": votes
    })


if __name__ == "__main__":
    app.run(debug=True)