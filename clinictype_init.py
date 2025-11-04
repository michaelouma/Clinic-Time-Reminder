from flask_app import create_app, db   # use the name of your main app file
from models import ClinicType

app = create_app()

with app.app_context():
    if not ClinicType.query.filter_by(name='HTN').first():
        db.session.add(ClinicType(name='HTN'))
    
    if not ClinicType.query.filter_by(name='DM').first():
        db.session.add(ClinicType(name='DM'))

    db.session.commit()
    print("HTN and DM clinic types initialized successfully.")
