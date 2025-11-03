import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from models import db, Patient, ClinicType

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'devkey')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///clinic.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def index():
        # search and filter
        search = request.args.get('search', '').strip()
        clinic_filter = request.args.get('clinic', '')
        page = int(request.args.get('page', 1))
        per_page = 10

        query = Patient.query.order_by(Patient.next_appointment.asc(), Patient.name.asc())


        if search:
            query = query.filter(Patient.name.ilike(f'%{search}%'))

        if clinic_filter:
            query = query.join(Patient.clinic_types).filter(ClinicType.id == int(clinic_filter))

        total = query.count()
        patients = query.offset((page-1)*per_page).limit(per_page).all()
        clinic_types = ClinicType.query.order_by(ClinicType.name).all()

        return render_template('index.html', patients=patients, clinic_types=clinic_types,
                               search=search, clinic_filter=clinic_filter, page=page, per_page=per_page, total=total)

    @app.route('/add', methods=['GET', 'POST'])
    def add_patient():
        clinic_types = ClinicType.query.order_by(ClinicType.name).all()
        if request.method == 'POST':
            name = request.form['name'].strip()
            phone = request.form.get('phone', '').strip()
            next_appointment = request.form.get('next_appointment') or None
            selected_ct = request.form.getlist('clinic_type')  # list of clinic type ids

            patient = Patient(name=name, phone=phone)
            if next_appointment:
                patient.next_appointment = datetime.fromisoformat(next_appointment)

            if selected_ct:
                for ct_id in selected_ct:
                    ct = ClinicType.query.get(int(ct_id))
                    if ct:
                        patient.clinic_types.append(ct)

            db.session.add(patient)
            db.session.commit()
            flash('Patient added', 'success')
            return redirect(url_for('index'))
        return render_template('add.html', clinic_types=clinic_types)

    @app.route('/edit/<int:patient_id>', methods=['GET', 'POST'])
    def edit_patient(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        clinic_types = ClinicType.query.order_by(ClinicType.name).all()
        if request.method == 'POST':
            patient.name = request.form['name'].strip()
            patient.phone = request.form.get('phone', '').strip()
            next_appointment = request.form.get('next_appointment') or None
            patient.next_appointment = datetime.fromisoformat(next_appointment) if next_appointment else None

            # update clinic types (many-to-many)
            selected_ct = [int(x) for x in request.form.getlist('clinic_type')]
            patient.clinic_types = [ClinicType.query.get(ct_id) for ct_id in selected_ct if ClinicType.query.get(ct_id)]

            db.session.commit()
            flash('Patient updated', 'success')
            return redirect(url_for('index'))
        return render_template('edit.html', patient=patient, clinic_types=clinic_types)

    @app.route('/delete/<int:patient_id>', methods=['POST'])
    def delete_patient(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        flash('Patient deleted', 'info')
        return redirect(url_for('index'))

    # quick update TCA endpoint (from index form)
    @app.route('/update_tca/<int:patient_id>', methods=['POST'])
    def update_tca(patient_id):
        patient = Patient.query.get_or_404(patient_id)
        next_appointment = request.form.get('next_appointment')
        if next_appointment:
            patient.next_appointment = datetime.fromisoformat(next_appointment)
            patient.status = 'Pending'
            db.session.commit()
            flash('Next appointment updated', 'success')
        else:
            flash('No date provided', 'warning')
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    app = create_app()
    # If development and DB doesn't exist, create tables - safe on first run
    with app.app_context():
        db.create_all()
    app.run(debug=True)
