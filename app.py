from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super_secret_key"  # needed for session login

# institution login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # simple fixed login check (you can replace with DB later)
        if username == "admin" and password == "password123":
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return "❌ Invalid credentials", 401

    # if GET → show login form
    return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        rollno = request.form["rollno"]
        name = request.form["name"]
        dept = request.form["dept"]
        lang = request.form["lang"]

        # normally you’d save student details in DB
        return redirect(url_for("student_page", rollno=rollno, lang=lang))

    return render_template("form.html")


@app.route("/student/<rollno>")
def student_page(rollno):
    pdf_url = f"/static/reports/{rollno}.pdf"
    return render_template("student.html", pdf_url=pdf_url, rollno=rollno)


if __name__ == "__main__":
    app.run(debug=True)












