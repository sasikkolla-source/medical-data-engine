"""
Populate the database with sample patients and medical records.
Run with: python seed_data.py
"""

from datetime import date, datetime, timedelta
import random

from app import create_app
from app.models import db, Patient, MedicalRecord

app = create_app()

SAMPLE_PATIENTS = [
    {"first_name": "Asha", "last_name": "Rao", "date_of_birth": date(1990, 4, 12),
     "gender": "Female", "blood_type": "O+", "contact_number": "9876543210",
     "email": "asha.rao@example.com"},
    {"first_name": "Vikram", "last_name": "Singh", "date_of_birth": date(1985, 11, 2),
     "gender": "Male", "blood_type": "B+", "contact_number": "9876543211",
     "email": "vikram.singh@example.com"},
    {"first_name": "Meera", "last_name": "Nair", "date_of_birth": date(2001, 7, 23),
     "gender": "Female", "blood_type": "A-", "contact_number": "9876543212",
     "email": "meera.nair@example.com"},
]

DIAGNOSES = ["Hypertension", "Type 2 Diabetes", "Common Cold", "Migraine", None]
RECORD_TYPES = ["checkup", "lab", "emergency", "follow-up"]


def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        patients = []
        for p in SAMPLE_PATIENTS:
            patient = Patient(**p)
            db.session.add(patient)
            patients.append(patient)
        db.session.commit()

        for patient in patients:
            for i in range(random.randint(2, 4)):
                visit_date = datetime.utcnow() - timedelta(days=random.randint(1, 365))
                record = MedicalRecord(
                    patient_id=patient.id,
                    visit_date=visit_date,
                    record_type=random.choice(RECORD_TYPES),
                    diagnosis=random.choice(DIAGNOSES),
                    notes="Routine visit, no immediate concerns.",
                    heart_rate=random.randint(60, 100),
                    blood_pressure_sys=random.randint(110, 140),
                    blood_pressure_dia=random.randint(70, 90),
                    temperature=round(random.uniform(36.1, 38.0), 1),
                    weight_kg=round(random.uniform(55, 95), 1),
                    height_cm=round(random.uniform(155, 185), 1),
                )
                db.session.add(record)
        db.session.commit()

        print(f"Seeded {len(patients)} patients with sample medical records.")


if __name__ == "__main__":
    seed()
