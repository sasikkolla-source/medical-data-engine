# Medical Data Engine

A simple, extensible base for managing and analyzing medical data — patients,
visit records, vitals, and basic analytics — built with Flask + SQLAlchemy + SQLite.

## Features

- **Patient management**: create, read, update, delete patient profiles
- **Medical records**: log visits with vitals (heart rate, blood pressure,
  temperature, weight/height → auto-computed BMI), diagnosis, and notes
- **Analytics**: aggregate stats (age distribution, gender/blood-type
  breakdowns, top diagnoses, average vitals) and per-patient trend timelines
- **REST API**: JSON endpoints ready to plug into any frontend

## Project Structure

```
medical_data_engine/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/__init__.py   # Patient & MedicalRecord models
│   └── routes/
│       ├── patients.py      # Patient CRUD endpoints
│       ├── records.py       # Medical record CRUD endpoints
│       └── analytics.py     # Aggregate & trend analytics endpoints
├── data/                    # SQLite database file lives here
├── run.py                   # App entry point
├── seed_data.py             # Sample data generator
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
python seed_data.py     # optional: populate with sample data
python run.py           # starts server at http://localhost:5000
```

## API Reference

### Patients — `/api/patients`

| Method | Endpoint                     | Description                          |
|--------|-------------------------------|---------------------------------------|
| GET    | `/api/patients`               | List all patients (`?search=name`)   |
| GET    | `/api/patients/<id>`          | Get one patient (`?include_records=true`) |
| POST   | `/api/patients`               | Create a patient                     |
| PUT    | `/api/patients/<id>`          | Update a patient                     |
| DELETE | `/api/patients/<id>`          | Delete a patient                     |

**Create patient — example body:**
```json
{
  "first_name": "Asha",
  "last_name": "Rao",
  "date_of_birth": "1990-04-12",
  "gender": "Female",
  "blood_type": "O+",
  "contact_number": "9876543210",
  "email": "asha.rao@example.com"
}
```

### Records — `/api/records`

| Method | Endpoint                | Description                              |
|--------|--------------------------|--------------------------------------------|
| GET    | `/api/records`           | List records (`?patient_id=1` to filter)  |
| GET    | `/api/records/<id>`      | Get one record                            |
| POST   | `/api/records`           | Create a record                           |
| PUT    | `/api/records/<id>`      | Update a record                           |
| DELETE | `/api/records/<id>`      | Delete a record                           |

**Create record — example body:**
```json
{
  "patient_id": 1,
  "record_type": "checkup",
  "diagnosis": "Hypertension",
  "notes": "Prescribed lifestyle changes.",
  "heart_rate": 78,
  "blood_pressure_sys": 130,
  "blood_pressure_dia": 85,
  "temperature": 36.8,
  "weight_kg": 72.5,
  "height_cm": 170
}
```

### Analytics — `/api/analytics`

| Method | Endpoint                              | Description                          |
|--------|-----------------------------------------|----------------------------------------|
| GET    | `/api/analytics/overview`               | Aggregate stats across all patients   |
| GET    | `/api/analytics/patient/<id>/trends`    | Vitals/diagnosis timeline for a patient |

### Health check

`GET /api/health` → `{"status": "ok", "service": "Medical Data Engine"}`

## Extending This Base

This is intentionally a minimal foundation. Natural next steps:
- Add authentication/authorization (e.g. Flask-Login, JWT)
- Add input validation (e.g. Marshmallow or Pydantic)
- Swap SQLite for PostgreSQL for production use
- Add file/image attachments (e.g. scan uploads)
- Build a frontend (React/Vue) that consumes the REST API
- Add FHIR/HL7 import-export for interoperability with real EHR systems

## Disclaimer

This is a demo/educational base and is **not** HIPAA-compliant or
production-ready for real patient data out of the box. Add proper
encryption, access controls, and audit logging before handling real PHI.
