from app import create_app
from models import db, ClinicType

app = create_app()

with app.app_context():
    db.create_all()
    # seed clinic types if not present
    default_types = ['HTN', 'DM', 'ART', 'Pediatrics', 'General']
    for name in default_types:
        if not ClinicType.query.filter_by(name=name).first():
            ct = ClinicType(name=name)
            db.session.add(ct)
    db.session.commit()
    print("Database and clinic types ready.")
