from flask import Flask, render_template, request, redirect, url_for, session, send_file
from gtts import gTTS
import io, uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Dummy login credentials
INSTITUTION_USER = "admin"
INSTITUTION_PASS = "vels123"

# In-memory storage for student reports
reports = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == INSTITUTION_USER and password == INSTITUTION_PASS:
            session["logged_in"] = True
            return redirect(url_for("form"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        rollno = request.form["rollno"]
        name = request.form["name"]
        department = request.form["department"]
        marks = request.form["marks"]
        remarks = request.form["remarks"]
        lang = request.form["lang"]

        # Generate unique ID
        report_id = str(uuid.uuid4())

        # Store report in memory
        reports[report_id] = {
            "rollno": rollno,
            "name": name,
            "department": department,
            "marks": marks,
            "remarks": remarks,
            "lang": lang
        }

        # Return a page with the unique link
        return render_template("link.html", link=url_for("view_report", report_id=report_id, _external=True))

    return render_template("form.html")

@app.route("/report/<report_id>")
def view_report(report_id):
    report = reports.get(report_id)
    if not report:
        return "Report not found", 404
    return render_template("student.html", **report)

@app.route("/tts")
def tts():
    text = request.args.get("text", "")
    lang = request.args.get("lang", "en")
    lang_map = {"ta": "ta", "hi": "hi", "ml": "ml", "te": "te", "en": "en"}
    tts = gTTS(text=text, lang=lang_map.get(lang, "en"))
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return send_file(mp3_fp, mimetype="audio/mpeg")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)














