import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

excel_file = 'Book1.xlsx'
df = pd.read_excel(excel_file)

today = datetime.today().date()
tomorrow = today + timedelta(days=1)

# Reset Status for future appointments
df.loc[(df['Next Appointment'].dt.date > today) & (df['Status'] == 'Reminded'), 'Status'] = 'Pending'

# Filter patients due tomorrow
due_patients = df[(df['Next Appointment'].dt.date == tomorrow) & (df['Status'] == 'Pending')]

if not due_patients.empty:
    # Build email message
    message_body = "Dear Clinician,\n\nThe following patients have appointments tomorrow:\n\n"
    for index, row in due_patients.iterrows():
        message_body += f"{row['Patient Name']} - {row['Next Appointment'].date()} ({row['Clinic Type']})\n"
    message_body += "\nPlease follow up as needed.\n\nRegards,\nClinic System"

    # Email settings
    sender_email = "moketchus12@gmail.com"
    receiver_email = "michael.ouma2021@students.jkuat.ac.ke"
    password = "pmhf wifs ovmo eiaf"  # Gmail requires App Password

    msg = MIMEText(message_body)
    msg['Subject'] = "Clinic Reminders for Tomorrow"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    
    # Update Status → Reminded
    df.loc[due_patients.index, 'Status'] = 'Reminded'

# Save Excel
df.to_excel(excel_file, index=False)
print("Reminder script executed and statuses updated.")
