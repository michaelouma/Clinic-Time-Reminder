# Clinic Appointment Reminder Automation

This project is a **Python automation script** that sends **email reminders to clinicians** about patients who have upcoming appointments. It reads appointment data from an Excel file, identifies patients due **tomorrow**, and sends an automated email listing those patients. It also updates the appointment status in the Excel file to ensure no duplicate reminders.

---

## ✨ Features
- Reads patient appointment data from an Excel file using **pandas**.  
- Identifies patients with appointments scheduled **for tomorrow**.  
- Sends a reminder email to the clinician with patient details (name, date, clinic type).  
- Updates the appointment status (`Pending` → `Reminded`) to track notifications.  
- Resets `Reminded` status back to `Pending` for future appointments.  
- Saves the updated appointment data back to the Excel file.

---

## 📂 Project Structure
├── Book1.xlsx # Excel file containing appointment data  
├── reminder_script.py # Main Python script  
└── README.md # Project documentation


---

## 📊 Excel File Format
The Excel file (`Book1.xlsx`) should have at least the following columns:

- **Patient Name** → Name of the patient  
- **Next Appointment** → Date of the patient’s next appointment (must be a valid date)  
- **Clinic Type** → Type of clinic (e.g., Dental, General)  
- **Status** → Current reminder status (`Pending`, `Reminded`)  

---

## ⚙️ Requirements
- Python 3.8+  
- Libraries:
   Flask,
   Pandas e.t.c  
  ```bash
  pip install pandas openpyxl

## 📌 Example Email
Subject: Clinic Reminders for Tomorrow

Dear Clinician,

The following patients have appointments tomorrow:

John James - 2025-10-03 (HTN)  
Jane Jack - 2025-10-03 (DM)

Please follow up as needed.

Regards,
Clinic System

