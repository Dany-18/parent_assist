from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader
from gtts import gTTS

app = Flask(__name__)

# paths
REPORT_DIR = "static/reports"
LOGO_PATH = "static/images/logo.png"
os.makedirs(REPORT_DIR, exist_ok=True)

students = {}  # in-memory DB

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        standard = request.form["standard"]
        attendance = request.form["attendance"]
        fees = request.form["fees"]
        marks = request.form["marks"]
        remarks = request.form["remarks"]
        lang = request.form["lang"]

        # PDF generation
        filepath = os.path.join(REPORT_DIR, f"{roll}.pdf")
        c = canvas.Canvas(filepath, pagesize=letter)

        if os.path.exists(LOGO_PATH):
            c.drawImage(LOGO_PATH, 220, 720, width=150, height=80)

        c.setFont("Helvetica", 12)
        y = 680
        c.drawString(100, y, f"Name: {name}"); y -= 20
        c.drawString(100, y, f"Roll No: {roll}"); y -= 20
        c.drawString(100, y, f"Standard: {standard}"); y -= 20
        c.drawString(100, y, f"Attendance: {attendance}%"); y -= 20
        c.drawString(100, y, f"Fees Pending: {fees}"); y -= 20
        c.drawString(100, y, f"Marks: {marks}"); y -= 20
        c.drawString(100, y, f"Remarks: {remarks}"); y -= 20

        c.save()

        students[roll] = {"file": filepath, "lang": lang}
        return redirect(url_for("student_page", rollno=roll))

    return render_template("form.html")

@app.route("/student/<rollno>")
def student_page(rollno):
    if rollno not in students:
        return "Student not found", 404
    pdf_url = f"/static/reports/{rollno}.pdf"
    return render_template("student.html", pdf_url=pdf_url, rollno=rollno, lang=students[rollno]["lang"])

@app.route("/tts")
def tts():
    text = request.args.get("text", "")
    lang = request.args.get("lang", "ta")
    filepath = os.path.join(REPORT_DIR, "tts.mp3")
    gTTS(text=text, lang=lang).save(filepath)
    return send_file(filepath, mimetype="audio/mpeg")

@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    data = request.get_json()
    roll = data.get("rollno")
    q = data.get("question", "").lower()
    lang = data.get("lang", "ta")

    if roll not in students:
        return jsonify({"answer": "தவறான மாணவர் தகவல்"})

    reader = PdfReader(students[roll]["file"])
    text = "".join([p.extract_text() for p in reader.pages]) or ""

    if any(word in q for word in ["attend", "ஹாஜர்", "ഹാജർ", "హాజరు"]):
        return jsonify({"answer": f"Attendance: {text.split('Attendance: ')[1].split('%')[0]}%"})
    if any(word in q for word in ["fee", "பணம்", "ഫീസ്", "ఫీజు"]):
        return jsonify({"answer": f"Fees info: {text.split('Fees Pending: ')[1].splitlines()[0]}"})
    if any(word in q for word in ["mark", "மதிப்பெண்", "మార్క్", "മാർക്ക്"]):
        return jsonify({"answer": f"Marks: {text.split('Marks: ')[1].splitlines()[0]}"})
    if any(word in q for word in ["remark", "குறிப்பு", "గమనిక", "കുറിപ്പ്"]):
        return jsonify({"answer": f"Remarks: {text.split('Remarks: ')[1].splitlines()[0]}"})

    return jsonify({"answer": "மன்னிக்கவும், உங்கள் கேள்வியைப் புரிந்து கொள்ள முடியவில்லை."})

if __name__ == "__main__":
    app.run(debug=True)










