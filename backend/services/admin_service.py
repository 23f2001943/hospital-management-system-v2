from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from extensions import db
from models import User, Role, Doctor, Patient, Appointment
import uuid
from sqlalchemy import or_
from datetime import datetime
class AdminService:

    @staticmethod
    def add_doctor(data):

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        department_id = data.get("department_id")

        qualification = data.get("qualification")
        experience_years = data.get("experience_years")
        consultation_fee = data.get("consultation_fee")
        contact_number = data.get("contact_number")
        room_number = data.get("room_number")
        availability = data.get("availability")

        if not name or not email or not password or not department_id:
            return {"message": "Missing required fields"}, 400

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

        db.session.flush()

        doctor = Doctor(
            user_id=user.id,
            specialization_id=department_id,
            qualification=qualification,
            experience_years=experience_years,
            consultation_fee=consultation_fee,
            contact_number=contact_number,
            room_number=room_number,
            availability=availability
        )

        db.session.add(doctor)
        db.session.commit()

        return {"message": "Doctor added successfully"}, 201

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
    
    @staticmethod
    def get_doctors(name=None, specialization=None):

        query = Doctor.query.join(User)

        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))

        if specialization:
            query = query.filter(Doctor.specialization_id == specialization)

        doctors = query.all()

        result = []

        for doc in doctors:
            result.append({
                "doctor_id": doc.id,
                "name": doc.user.name,
                "email": doc.user.email,
                "department_id": doc.specialization_id,
                "department": doc.department.name if doc.department else None,
                "qualification": doc.qualification,
                "experience_years": doc.experience_years,
                "consultation_fee": float(doc.consultation_fee) if doc.consultation_fee else None,
                "contact_number": doc.contact_number,
                "room_number": doc.room_number,
                "availability": doc.availability,
                "is_active": doc.is_active
            })

        return result
    
    @staticmethod
    def update_doctor(doctor_id, data):

        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return {"message": "Doctor not found"}, 404

        doctor.specialization_id = data.get("department_id", doctor.specialization_id)
        doctor.qualification = data.get("qualification", doctor.qualification)
        doctor.experience_years = data.get("experience_years", doctor.experience_years)
        doctor.consultation_fee = data.get("consultation_fee", doctor.consultation_fee)
        doctor.contact_number = data.get("contact_number", doctor.contact_number)
        doctor.room_number = data.get("room_number", doctor.room_number)
        doctor.availability = data.get("availability", doctor.availability)

        db.session.commit()

        return {"message": "Doctor updated successfully"}, 200
    @staticmethod
    def blacklist_doctor(doctor_id):

        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return {"message": "Doctor not found"}, 404

        doctor.is_active = False
        db.session.commit()

        return {"message": "Doctor blacklisted successfully"}, 200
    
    @staticmethod
    def get_departments():
        from models import Department

        departments = Department.query.filter_by(is_active=True).all()

        return [
            {
                "id": dept.id,
                "name": dept.name
            }
            for dept in departments
        ]
    
    @staticmethod
    def delete_doctor(doctor_id):

        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return {"message": "Doctor not found"}, 404

        db.session.delete(doctor)
        db.session.commit()

        return {"message": "Doctor deleted permanently"}, 200
    

    @staticmethod
    def get_patients(name=None, patient_id=None, contact=None):

        query = Patient.query.join(User)

        # Search by name
        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))

        # Search by patient ID (exact match)
        if patient_id:
            query = query.filter(Patient.id == int(patient_id))

        # Search by contact number
        if contact:
            query = query.filter(Patient.contact_number.ilike(f"%{contact}%"))

        patients = query.all()

        result = []

        for p in patients:
            result.append({
                "patient_id": p.id,
                "name": p.user.name,
                "email": p.user.email,
                "gender": p.gender,
                "blood_group": p.blood_group,
                "contact_number": p.contact_number,
                "is_active": p.is_active
            })

        return result
    
    @staticmethod
    def blacklist_patient(patient_id):

        patient = Patient.query.get(patient_id)

        if not patient:
            return {"message": "Patient not found"}, 404

        patient.is_active = False
        db.session.commit()

        return {"message": "Patient blacklisted"}, 200
    
    @staticmethod
    def delete_patient(patient_id):

        patient = Patient.query.get(patient_id)

        if not patient:
            return {"message": "Patient not found"}, 404

        db.session.delete(patient)
        db.session.commit()

        return {"message": "Patient deleted permanently"}, 200
    
    @staticmethod
    def get_appointments(status=None):

        query = Appointment.query

        if status:
            query = query.filter(Appointment.status == status)

        appointments = query.all()

        result = []

        for appt in appointments:

            result.append({
    "appointment_id": appt.id,
    "doctor_name": appt.doctor.user.name if appt.doctor else None,
    "patient_name": appt.patient.user.name if appt.patient else None,
    "date": appt.date.strftime("%Y-%m-%d") if appt.date else None,
    "time": appt.time.strftime("%H:%M") if appt.time else None,
    "status": appt.status
})

        return result
    
    @staticmethod
    def cancel_appointment(appointment_id):

        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return {"message": "Appointment not found"}, 404

        appointment.status = "Cancelled"

        db.session.commit()

        return {"message": "Appointment cancelled"}, 200
    
    @staticmethod
    def update_appointment(appointment_id, data):

        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return {"message": "Appointment not found"}, 404

        if data.get("doctor_id"):
            appointment.doctor_id = data["doctor_id"]

        if data.get("patient_id"):
            appointment.patient_id = data["patient_id"]

        if data.get("date"):
            appointment.date = datetime.strptime(data["date"], "%Y-%m-%d").date()

        if data.get("time"):
            appointment.time = datetime.strptime(data["time"], "%H:%M").time()

        db.session.commit()

        return {"message": "Appointment updated"}, 200