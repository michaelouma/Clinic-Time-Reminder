import os
import smtplib
from email.mime.text import MIMEText
from datetime import date, timedelta
from dotenv import load_dotenv
from app import create_app
from models import db, Patient

load_dotenv()
app = create_app()

SENDER_EMAIL = os.getenv('GMAIL_SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('CLINICIAN_RECEIVER_EMAIL')
PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

def send_daily_reminder():
    with app.app_context():
        tomorrow = date.today() + timedelta(days=1)
        patients = Patient.query.filter(
            Patient.next_appointment.isnot(None)
        ).all()

        due = []
        for p in patients:
            if p.next_appointment.date() == tomorrow and p.status == 'Pending':
                due.append(p)

        if not due:
            print(f"No patients due on {tomorrow.isoformat()}")
            return

        body = f"Dear Clinician,\n\nThe following {len(due)} patients have appointments on {tomorrow.strftime('%Y-%m-%d')}:\n\n"
        for p in due:
            time_part = p.next_appointment.time().strftime('%H:%M') if p.next_appointment.time() else "N/A"
            body += f"- {p.name} at {time_part} ({p.clinic_types_str()}) - Phone: {p.phone}\n"

        body += "\nRegards,\nClinic System"

        msg = MIMEText(body)
        msg['Subject'] = f"Daily Reminder: {len(due)} Appointments on {tomorrow.strftime('%Y-%m-%d')}"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(SENDER_EMAIL, PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

            # update statuses
            for p in due:
                p.status = 'Reminded'
            db.session.commit()
            print(f"Sent reminder for {len(due)} patients.")
        except Exception as e:
            print("Error sending email:", e)

if __name__ == '__main__':
    send_daily_reminder()
