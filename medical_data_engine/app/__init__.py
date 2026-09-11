"""
Medical Data Engine
--------------------
A simple, extensible base for managing and analyzing medical data:
patients, visits, and vital/lab records.
"""

import os
from flask import Flask
from flask_cors import CORS

from app.models import db


def create_app(test_config=None):
    """Application factory."""
    app = Flask(__name__, instance_relative_config=True)

    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "medical_data.db")

    app.config.from_mapping(
        SECRET_KEY="dev",  # override in production via env var
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSON_SORT_KEYS=False,
    )

    if test_config:
        app.config.update(test_config)

    CORS(app)
    db.init_app(app)

    # Register blueprints
    from app.routes.patients import patients_bp
    from app.routes.records import records_bp
    from app.routes.analytics import analytics_bp

    app.register_blueprint(patients_bp, url_prefix="/api/patients")
    app.register_blueprint(records_bp, url_prefix="/api/records")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    @app.route("/api/health")
    def health():
        return {"status": "ok", "service": "Medical Data Engine"}

    with app.app_context():
        db.create_all()

    return app
