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
