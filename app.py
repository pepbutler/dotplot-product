import sqlite3
from sqlite3 import Connection

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config["SECRET_KEY"] = "kdfj92n9db29"


def get_db_connection() -> Connection:
    conn = sqlite3.connect("files/patient.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_patient(patient_id: int) -> dict:
    conn = get_db_connection()
    patient = conn.execute(
        "SELECT * FROM patient WHERE id = ?", (patient_id,)
    ).fetchone()
    conn.close()
    if patient is None:
        abort(404)
    return patient


@app.route("/")
def index():
    # TODO: add explaining text to the html file
    return render_template("index.html")


@app.route("/new_patient", methods=("GET", "POST"))
def new_patient():
    if request.method == "POST":
        print(request.form)
        name = request.form["name"]
        height = request.form["height"]
        weight = request.form["weight"]
        age = request.form["age"]
        has_history = request.form["has_history"]
        if not any((name, height, weight, age, has_history)):
            flash("Please fill all the field!")
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO patient (name,age,height,weight,history) VALUES (?, ?, ?, ?, ?)",
                (
                    name,
                    int(height),
                    int(weight),
                    int(age),
                    bool(has_history),
                ),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("patients"))
    return render_template("new_patient.html")


@app.route("/patient/edit/<int:patient_id>", methods=("GET", "POST"))
def edit_patient(patient_id):
    patient = get_patient(patient_id)

    if request.method == "POST":
        name = request.form["name"]
        height = request.form["height"]
        weight = request.form["weight"]
        age = request.form["age"]
        has_history = request.form["has_history"]
        conn = get_db_connection()
        conn.execute(
            "UPDATE patient SET name = ?, height = ?, weight = ?, age = ?, history= ? WHERE id = ?",
            (
                name,
                int(height),
                int(weight),
                int(age),
                has_history.lower().startswith("y"),
                patient_id,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("edit_patient.html", patient=patient)


@app.route("/patient/delete/<int:patient_id>", methods=("POST",))
def delete_patient(patient_id):
    post = get_patient(patient_id)
    conn = get_db_connection()
    conn.execute("DELETE FROM patient WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post["name"]))
    return redirect(url_for("index"))


@app.route("/patients")
def patients():
    conn = get_db_connection()
    patients = conn.execute("SELECT * FROM patient").fetchall()
    patients.pop(0)
    conn.close()
    return render_template("patients.html", patients=patients)


@app.route("/patient/<int:patient_id>")
def patient(patient_id):
    return render_template("patient.html", patient=get_patient(patient_id))


@app.route("/scans")
def scans():
    conn = get_db_connection()
    scans = conn.execute("SELECT * FROM scan").fetchall()
    scans.pop(0)
    conn.close()
    return render_template("scans.html", scans=scans)


@app.route("/viewer")
def viewer():
    return render_template("viewer.html")
