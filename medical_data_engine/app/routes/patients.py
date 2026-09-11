from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models import db, Patient

patients_bp = Blueprint("patients", __name__)


@patients_bp.route("", methods=["GET"])
def list_patients():
    search = request.args.get("search", "").strip()
    query = Patient.query
    if search:
        like = f"%{search}%"
        query = query.filter(
            (Patient.first_name.ilike(like)) | (Patient.last_name.ilike(like))
        )
    patients = query.order_by(Patient.last_name).all()
    return jsonify([p.to_dict() for p in patients])


@patients_bp.route("/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    include_records = request.args.get("include_records", "false").lower() == "true"
    return jsonify(patient.to_dict(include_records=include_records))


@patients_bp.route("", methods=["POST"])
def create_patient():
    data = request.get_json(force=True) or {}

    required = ["first_name", "last_name", "date_of_birth"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        dob = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "date_of_birth must be in YYYY-MM-DD format"}), 400

    patient = Patient(
        first_name=data["first_name"],
        last_name=data["last_name"],
        date_of_birth=dob,
        gender=data.get("gender"),
        blood_type=data.get("blood_type"),
        contact_number=data.get("contact_number"),
        email=data.get("email"),
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201


@patients_bp.route("/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json(force=True) or {}

    for field in ["first_name", "last_name", "gender", "blood_type", "contact_number", "email"]:
        if field in data:
            setattr(patient, field, data[field])

    if "date_of_birth" in data:
        try:
            patient.date_of_birth = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "date_of_birth must be in YYYY-MM-DD format"}), 400

    db.session.commit()
    return jsonify(patient.to_dict())


@patients_bp.route("/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": f"Patient {patient_id} deleted"})
