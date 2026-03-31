from flask import Flask
from config import LocalDevelopmentConfig
from extensions import db,security
from models import User, Role
from flask_security.datastore import SQLAlchemyUserDatastore
from resources import auth_bp, admin_bp , doctor_bp, patient_bp
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    CORS(
    app,
    supports_credentials=True,
    expose_headers=["Content-Type", "Authentication-Token"],
    allow_headers=["Content-Type", "Authentication-Token"]
)
    app.config.from_object(LocalDevelopmentConfig)

    # initialize database
    db.init_app(app)
    datastore=SQLAlchemyUserDatastore(db,User,Role)
    security.init_app(app,datastore)

    app.datastore=datastore

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)

    # create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
