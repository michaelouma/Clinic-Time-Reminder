# send_reminders.py

import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta, date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration ---
SENDER_EMAIL = os.environ.get('GMAIL_SENDER_EMAIL')
RECEIVER_EMAIL = os.environ.get('CLINICIAN_RECEIVER_EMAIL')
PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')
EXCEL_FILE = os.environ.get('EXCEL_FILE', 'Book1.xlsx')
# ---------------------

def send_daily_reminder():
    if not os.path.exists(EXCEL_FILE):
        print(f"[{datetime.now()}] ERROR: Excel file '{EXCEL_FILE}' not found. Cannot send reminders.")
        return

    try:
        # Load Data, ensuring date column is correctly parsed
        df = pd.read_excel(EXCEL_FILE, parse_dates=['Next Appointment'])
    except Exception as e:
        print(f"[{datetime.now()}] ERROR reading Excel file: {e}")
        return

    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # 1. Reset 'Reminded' status if appointment was rescheduled far into the future (optional but robust)
    df.loc[(df['Next Appointment'].dt.date > today) & (df['Status'] == 'Reminded'), 'Status'] = 'Pending'

    # 2. Filter patients due tomorrow and still 'Pending'
    due_patients_mask = (df['Next Appointment'].dt.date == tomorrow) & (df['Status'] == 'Pending')
    due_patients = df[due_patients_mask]

    if due_patients.empty:
        print(f"[{datetime.now()}] No new patients due tomorrow, {tomorrow.isoformat()}. Email not sent.")
        return

    # 3. Build Email Message
    message_body = f"Dear Clinician,\n\nThe following {len(due_patients)} patients have appointments tomorrow, {tomorrow.strftime('%Y-%m-%d')}:\n\n"
    
    for index, row in due_patients.iterrows():
        # Get time from the datetime object for better context
        appt_time = row['Next Appointment'].time().strftime('%H:%M')
        message_body += f"- {row['Patient Name']} at {appt_time} ({row['Clinic Type']})\n"
        
    message_body += "\nPlease review their files.\n\nRegards,\nClinic System"

    # 4. Send Email
    try:
        msg = MIMEText(message_body)
        msg['Subject'] = f"Daily Reminder: {len(due_patients)} Appointments for Tomorrow"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        
        # 5. Update Status in Excel (CRUCIAL step!)
        df.loc[due_patients_mask, 'Status'] = 'Reminded'
        df.to_excel(EXCEL_FILE, index=False)

        print(f"[{datetime.now()}] Successfully sent reminder for {len(due_patients)} patients.")

    except Exception as e:
        print(f"[{datetime.now()}] FATAL ERROR: Failed to send email or update Excel: {e}")


if __name__ == "__main__":
    send_daily_reminder()