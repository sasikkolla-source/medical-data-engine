from flask import Blueprint, request, jsonify
from app.models import db, MedicalRecord, Patient

records_bp = Blueprint("records", __name__)


@records_bp.route("", methods=["GET"])
def list_records():
    patient_id = request.args.get("patient_id", type=int)
    query = MedicalRecord.query
    if patient_id:
        query = query.filter_by(patient_id=patient_id)
    records = query.order_by(MedicalRecord.visit_date.desc()).all()
    return jsonify([r.to_dict() for r in records])


@records_bp.route("/<int:record_id>", methods=["GET"])
def get_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    return jsonify(record.to_dict())


@records_bp.route("", methods=["POST"])
def create_record():
    data = request.get_json(force=True) or {}

    patient_id = data.get("patient_id")
    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400

    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": f"No patient found with id {patient_id}"}), 404

    record = MedicalRecord(
        patient_id=patient_id,
        record_type=data.get("record_type", "general"),
        diagnosis=data.get("diagnosis"),
        notes=data.get("notes"),
        heart_rate=data.get("heart_rate"),
        blood_pressure_sys=data.get("blood_pressure_sys"),
        blood_pressure_dia=data.get("blood_pressure_dia"),
        temperature=data.get("temperature"),
        weight_kg=data.get("weight_kg"),
        height_cm=data.get("height_cm"),
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201


@records_bp.route("/<int:record_id>", methods=["PUT"])
def update_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    data = request.get_json(force=True) or {}

    editable = [
        "record_type", "diagnosis", "notes", "heart_rate",
        "blood_pressure_sys", "blood_pressure_dia",
        "temperature", "weight_kg", "height_cm",
    ]
    for field in editable:
        if field in data:
            setattr(record, field, data[field])

    db.session.commit()
    return jsonify(record.to_dict())


@records_bp.route("/<int:record_id>", methods=["DELETE"])
def delete_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": f"Record {record_id} deleted"})
