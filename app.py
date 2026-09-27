from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "portfolio-secret-key"

DATABASE = "portfolio.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            technologies TEXT NOT NULL,
            github TEXT,
            demo TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    project_count = connection.execute(
        "SELECT COUNT(*) FROM projects"
    ).fetchone()[0]

    if project_count == 0:
        projects = [
            (
                "Student Study Planner",
                "A web application that helps students organize subjects, tasks and study schedules.",
                "HTML, CSS, JavaScript, Flask",
                "https://github.com/",
                "#"
            ),
            (
                "Smart Agriculture Decision System",
                "An AI-based project idea for helping farmers make better agricultural decisions using data.",
                "Python, AI, Machine Learning",
                "https://github.com/",
                "#"
            ),
            (
                "Personal Portfolio",
                "A full-stack personal portfolio website built to showcase my skills, education and projects.",
                "HTML, CSS, JavaScript, Flask, SQLite",
                "https://github.com/",
                "#"
            )
        ]

        connection.executemany("""
            INSERT INTO projects
            (title, description, technologies, github, demo)
            VALUES (?, ?, ?, ?, ?)
        """, projects)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    connection = get_db_connection()

    projects = connection.execute(
        "SELECT * FROM projects ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template("index.html", projects=projects)


@app.route("/contact", methods=["POST"])
def contact():

    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("Please fill in all fields.")
        return redirect(url_for("home"))

    connection = get_db_connection()

    connection.execute("""
        INSERT INTO messages (name, email, message)
        VALUES (?, ?, ?)
    """, (name, email, message))

    connection.commit()
    connection.close()

    flash("Your message has been sent successfully!")

    return redirect(url_for("home") + "#contact")


if __name__ == "__main__":
    initialize_database()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )