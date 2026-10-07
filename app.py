from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "portfolio.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "portfolio-secret-key")


def get_db_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    connection = get_db_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                technologies TEXT NOT NULL,
                github TEXT,
                demo TEXT
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        project_count = connection.execute("SELECT COUNT(*) FROM projects").fetchone()[0]

        if project_count == 0:
            projects = [
                (
                    "Student Study Planner",
                    "A web application that helps students organize subjects, tasks and study schedules.",
                    "HTML, CSS, JavaScript, Flask",
                    "https://github.com/",
                    "#",
                ),
                (
                    "Smart Agriculture Decision System",
                    "An AI-based project idea for helping farmers make better agricultural decisions using data.",
                    "Python, AI, Machine Learning",
                    "https://github.com/",
                    "#",
                ),
                (
                    "Personal Portfolio",
                    "A full-stack personal portfolio website built to showcase my skills, education and projects.",
                    "HTML, CSS, JavaScript, Flask, SQLite",
                    "https://github.com/",
                    "#",
                ),
            ]

            connection.executemany(
                """
                INSERT INTO projects (title, description, technologies, github, demo)
                VALUES (?, ?, ?, ?, ?)
                """,
                projects,
            )

        connection.commit()
    finally:
        connection.close()


@app.route("/")
def home():
    connection = get_db_connection()

    try:
        projects = connection.execute(
            "SELECT * FROM projects ORDER BY id DESC"
        ).fetchall()
    finally:
        connection.close()

    return render_template("index.html", projects=projects)


@app.route("/contact", methods=["POST"])
def contact():
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    message = (request.form.get("message") or "").strip()

    if not all([name, email, message]):
        flash("Please fill in all fields.", "error")
        return redirect(url_for("home") + "#contact")

    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("home") + "#contact")

    connection = get_db_connection()

    try:
        connection.execute(
            """
            INSERT INTO messages (name, email, message)
            VALUES (?, ?, ?)
            """,
            (name, email, message),
        )
        connection.commit()
    finally:
        connection.close()

    flash("Thanks for reaching out! Your message has been sent.", "success")
    return redirect(url_for("home") + "#contact")


initialize_database()


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
    )
