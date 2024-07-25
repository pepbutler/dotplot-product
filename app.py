import sqlite3
from sqlite3 import Connection

from flask import Flask, render_template

app = Flask(__name__)


def get_db_connection() -> Connection:
    conn = sqlite3.connect("files/patient.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    # TODO: add explaining text to the html file
    return render_template("index.html")


@app.route("/patients")
def patients():
    conn = get_db_connection()
    patients = conn.execute("SELECT * FROM patient").fetchall()
    patients.pop(0)
    conn.close()
    return render_template("patients.html", patients=patients)


@app.route("/scans")
def scans():
    return render_template("scans.html")


@app.route("/viewer")
def viewer():
    return render_template("viewer.html")
