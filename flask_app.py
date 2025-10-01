from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)
excel_file = 'Book1.xlsx'

# Homepage: search and display patients
@app.route('/')
def index():
    df = pd.read_excel(excel_file)
    search_name = request.args.get('search')
    if search_name:
        df = df[df['Patient Name'].str.contains(search_name, case=False)]
    patients = df.to_dict(orient='records')
    return render_template('index.html', patients=patients)

# Update patient's next appointment
@app.route('/update', methods=['POST'])
def update():
    name = request.form['name']
    new_date = request.form['next_appointment']
    df = pd.read_excel(excel_file)
    df.loc[df['Patient Name'] == name, 'Next Appointment'] = pd.to_datetime(new_date)
    df.loc[df['Patient Name'] == name, 'Status'] = 'Pending'  # Reset status automatically
    df.to_excel(excel_file, index=False)
    return redirect('/')

# Add new patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        next_appointment = request.form['next_appointment']
        clinic_type = request.form['clinic_type']

        df = pd.read_excel(excel_file)
        new_row = {
            'Patient Name': name,
            'Phone': phone,
            'Next Appointment': pd.to_datetime(next_appointment),
            'Status': 'Pending',
            'Clinic Type': clinic_type
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(excel_file, index=False)
        return redirect('/')
    return render_template('add.html')

if __name__ == "__main__":
    app.run(debug=True)
