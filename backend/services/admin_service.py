from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from extensions import db
from models import User, Role, Doctor, Patient, Appointment
import uuid


class AdminService:

    @staticmethod
    def add_doctor(data):

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        department_id = data.get("department_id")

        if not name or not email or not password or not department_id:
            return {"message": "Missing fields"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "Doctor already exists"}, 400

        datastore = SQLAlchemyUserDatastore(db, User, Role)

        user = datastore.create_user(
            name=name,
            email=email,
            password=hash_password(password),
            fs_uniquifier=str(uuid.uuid4()),
            active=True
        )

        doctor_role = datastore.find_role("doctor")
        datastore.add_role_to_user(user, doctor_role)

        db.session.flush()  # ensure user.id available

        doctor = Doctor(
            user_id=user.id,
            specialization_id=department_id
        )

        db.session.add(doctor)
        db.session.commit()

        return {
            "message": "Doctor added successfully",
            "doctor_id": user.id
        }, 201

    @staticmethod
    def get_dashboard_stats():

        total_doctors = Doctor.query.filter_by(is_active=True).count()
        total_patients = Patient.query.filter_by(is_active=True).count()
        total_appointments = Appointment.query.count()

        booked = Appointment.query.filter_by(status="Booked").count()
        completed = Appointment.query.filter_by(status="Completed").count()
        cancelled = Appointment.query.filter_by(status="Cancelled").count()

        return {
            "total_doctors": total_doctors,
            "total_patients": total_patients,
            "total_appointments": total_appointments,
            "booked": booked,
            "completed": completed,
            "cancelled": cancelled
        }