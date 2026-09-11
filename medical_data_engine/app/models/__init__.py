from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20))
    blood_type = db.Column(db.String(5))
    contact_number = db.Column(db.String(30))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    records = db.relationship(
        "MedicalRecord", backref="patient", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def to_dict(self, include_records=False):
        data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.isoformat(),
            "age": self.age,
            "gender": self.gender,
            "blood_type": self.blood_type,
            "contact_number": self.contact_number,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }
        if include_records:
            data["records"] = [r.to_dict() for r in self.records]
        return data


class MedicalRecord(db.Model):
    """A single visit/encounter record with vitals and notes."""

    __tablename__ = "medical_records"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)

    visit_date = db.Column(db.DateTime, default=datetime.utcnow)
    record_type = db.Column(db.String(50), default="general")  # e.g. checkup, lab, emergency
    diagnosis = db.Column(db.String(255))
    notes = db.Column(db.Text)

    # Vitals
    heart_rate = db.Column(db.Integer)          # bpm
    blood_pressure_sys = db.Column(db.Integer)   # mmHg
    blood_pressure_dia = db.Column(db.Integer)   # mmHg
    temperature = db.Column(db.Float)            # Celsius
    weight_kg = db.Column(db.Float)
    height_cm = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def bmi(self):
        if self.weight_kg and self.height_cm:
            height_m = self.height_cm / 100
            return round(self.weight_kg / (height_m ** 2), 2)
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "visit_date": self.visit_date.isoformat(),
            "record_type": self.record_type,
            "diagnosis": self.diagnosis,
            "notes": self.notes,
            "heart_rate": self.heart_rate,
            "blood_pressure": f"{self.blood_pressure_sys}/{self.blood_pressure_dia}"
            if self.blood_pressure_sys and self.blood_pressure_dia
            else None,
            "temperature": self.temperature,
            "weight_kg": self.weight_kg,
            "height_cm": self.height_cm,
            "bmi": self.bmi,
            "created_at": self.created_at.isoformat(),
        }
