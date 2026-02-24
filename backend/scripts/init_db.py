from app import app
from extensions import db
from models import User, Role
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

with app.app_context():
    db.drop_all()
    db.create_all()
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    admin_role = datastore.find_or_create_role(
    name="admin",
    description="Hospital Administrator"
    )

    doctor_role = datastore.find_or_create_role(
        name="doctor",
        description="Hospital Doctor"
    )

    patient_role = datastore.find_or_create_role(
        name="patient",
        description="Hospital Patient"
    )
    if not datastore.find_user(email="admin@hospital.com"):
        admin_user = datastore.create_user(
            email="admin@hospital.com",
            name="Hospital Admin",
            password=hash_password("admin123"),
            active=True
        )
        datastore.add_role_to_user(admin_user, admin_role)
        try:
            db.session.commit()
            print("Admin and roles created successfully")
        except Exception as e:
            db.session.rollback()
            print(" Error during DB init:", e)