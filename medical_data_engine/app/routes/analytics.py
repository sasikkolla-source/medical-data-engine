from collections import Counter
from statistics import mean, median, StatisticsError

from flask import Blueprint, jsonify
from app.models import Patient, MedicalRecord

analytics_bp = Blueprint("analytics", __name__)


def _safe_mean(values):
    values = [v for v in values if v is not None]
    try:
        return round(mean(values), 2)
    except StatisticsError:
        return None


def _safe_median(values):
    values = [v for v in values if v is not None]
    try:
        return round(median(values), 2)
    except StatisticsError:
        return None


@analytics_bp.route("/overview", methods=["GET"])
def overview():
    patients = Patient.query.all()
    records = MedicalRecord.query.all()

    ages = [p.age for p in patients]
    genders = Counter(p.gender for p in patients if p.gender)
    blood_types = Counter(p.blood_type for p in patients if p.blood_type)
    diagnoses = Counter(r.diagnosis for r in records if r.diagnosis)
    record_types = Counter(r.record_type for r in records if r.record_type)

    heart_rates = [r.heart_rate for r in records]
    temperatures = [r.temperature for r in records]
    bmis = [r.bmi for r in records if r.bmi]

    return jsonify({
        "total_patients": len(patients),
        "total_records": len(records),
        "age": {
            "average": _safe_mean(ages),
            "median": _safe_median(ages),
            "min": min(ages) if ages else None,
            "max": max(ages) if ages else None,
        },
        "gender_distribution": dict(genders),
        "blood_type_distribution": dict(blood_types),
        "top_diagnoses": diagnoses.most_common(5),
        "record_type_distribution": dict(record_types),
        "vitals": {
            "avg_heart_rate": _safe_mean(heart_rates),
            "avg_temperature": _safe_mean(temperatures),
            "avg_bmi": _safe_mean(bmis),
        },
    })


@analytics_bp.route("/patient/<int:patient_id>/trends", methods=["GET"])
def patient_trends(patient_id):
    records = (
        MedicalRecord.query.filter_by(patient_id=patient_id)
        .order_by(MedicalRecord.visit_date.asc())
        .all()
    )
    if not records:
        return jsonify({"error": "No records found for this patient"}), 404

    return jsonify({
        "patient_id": patient_id,
        "visit_count": len(records),
        "timeline": [
            {
                "visit_date": r.visit_date.isoformat(),
                "heart_rate": r.heart_rate,
                "temperature": r.temperature,
                "bmi": r.bmi,
                "diagnosis": r.diagnosis,
            }
            for r in records
        ],
    })
