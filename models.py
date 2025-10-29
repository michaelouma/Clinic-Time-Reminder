from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# association table for many-to-many patient <-> clinic types
patient_clinictype = db.Table(
    'patient_clinictype',
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.id'), primary_key=True),
    db.Column('clinictype_id', db.Integer, db.ForeignKey('clinic_types.id'), primary_key=True)
)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(40))
    next_appointment = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default='Pending')  # Pending, Reminded, Completed, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    clinic_types = db.relationship('ClinicType', secondary=patient_clinictype, back_populates='patients')

    def clinic_types_str(self):
        return ', '.join([ct.name for ct in self.clinic_types])

class ClinicType(db.Model):
    __tablename__ = 'clinic_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    patients = db.relationship('Patient', secondary=patient_clinictype, back_populates='clinic_types')
