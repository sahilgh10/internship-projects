from flask import Flask, render_template, request, redirect
import sqlite3
import threading
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
import time

app = Flask(__name__)
DATABASE = 'reminders.db'

# === Email credentials ===
SENDER_EMAIL = "thelev2107@gmail.com"
SENDER_PASSWORD = "wosr nswn wabk bxzl"  # Use your actual 16-character Gmail App Password

# === Initialize DB ===
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                subject TEXT,
                body TEXT,
                date TEXT,
                time TEXT,
                type TEXT
            )
        ''')

# === Background email thread ===
def check_and_send_reminders():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM reminders WHERE date || ' ' || time = ?", (now,))
            due = cur.fetchall()
            for r in due:
                send_email(r[1], r[2], r[3])
                cur.execute("DELETE FROM reminders WHERE id = ?", (r[0],))
            conn.commit()
        time.sleep(60)

# === Send Email ===
def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("✅ Email sent to", to_email)
    except Exception as e:
        print("❌ Failed to send email:", e)

# === Routes ===
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        subject_input = request.form["subject"].strip()
        date_val = request.form["date"]
        time_val = request.form["time"]
        type_val = request.form["type"]

        # === Auto-generate body based on subject keywords ===
        subject = subject_input.lower()
        if "meeting" in subject:
            body = "This is a reminder that your scheduled meeting is about to begin. Please be prepared."
        elif "task" in subject:
            body = "This is a reminder to complete your pending task on time."
        elif "deadline" in subject:
            body = "Reminder: You have an upcoming deadline. Please ensure all deliverables are ready."
        else:
            body = f"This is a scheduled reminder for: {subject_input}"

        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                "INSERT INTO reminders (email, subject, body, date, time, type) VALUES (?, ?, ?, ?, ?, ?)",
                (email, subject_input, body, date_val, time_val, type_val)
            )
        return redirect("/")

    # GET request
    with sqlite3.connect(DATABASE) as conn:
        reminders = conn.execute("SELECT * FROM reminders ORDER BY date, time").fetchall()
    return render_template("form.html", reminders=reminders)

# === Start ===
init_db()
threading.Thread(target=check_and_send_reminders, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)