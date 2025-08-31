from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for login session

# Hardcoded institution login (you can replace with DB later)
USERS = {
    "admin": "vels123",
    "teacher": "teacher123"
}

# ---------------- LOGIN SYSTEM ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="❌ Invalid username or password")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    # institution dashboard (form to enter student roll number)
    return render_template("form.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ---------------- STUDENT REPORT ----------------
@app.route("/student/<rollno>")
def student_page(rollno):
    if "user" not in session:
        return redirect(url_for("login"))

    pdf_url = f"/static/reports/{rollno}.pdf"
    # Default language = Tamil (you can expand)
    return render_template("student.html", pdf_url=pdf_url, rollno=rollno, lang="ta")

# ------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)












