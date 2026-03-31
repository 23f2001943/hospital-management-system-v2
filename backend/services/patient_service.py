from models import Patient
from extensions import db
from flask_security import current_user
from models import Doctor, User, Department, Appointment, Patient
from datetime import datetime

class PatientService:

    @staticmethod
    def get_patient():
        return Patient.query.filter_by(user_id=current_user.id).first()

    @staticmethod
    def get_profile():
        patient = PatientService.get_patient()

        if not patient:
            return {"message": "Patient not found"}, 404

        return {
            "patient_id": patient.id,
            "name": patient.user.name,
            "email": patient.user.email,
            "gender": patient.gender,
            "blood_group": patient.blood_group,
            "contact_number": patient.contact_number,
            "emergency_contact": patient.emergency_contact,
            "address": patient.address,
            "date_of_birth": patient.date_of_birth.strftime("%Y-%m-%d") if patient.date_of_birth else None
        }, 200

    @staticmethod
    def update_profile(data):
        patient = PatientService.get_patient()

        if not patient:
            return {"message": "Patient not found"}, 404

        # update User table fields
        if data.get("name"):
            patient.user.name = data["name"]

        # update Patient table fields
        patient.gender = data.get("gender", patient.gender)
        patient.blood_group = data.get("blood_group", patient.blood_group)
        patient.contact_number = data.get("contact_number", patient.contact_number)
        patient.emergency_contact = data.get("emergency_contact", patient.emergency_contact)
        patient.address = data.get("address", patient.address)

        if data.get("date_of_birth"):
            from datetime import datetime
            patient.date_of_birth = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()

        db.session.commit()

        return {"message": "Profile updated successfully"}, 200
    
    

    @staticmethod
    def get_doctors(name=None, specialization=None):

        query = Doctor.query.join(User).join(Department)

        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))

        if specialization:
            query = query.filter(
                Department.name.ilike(f"%{specialization}%")
            )

        doctors = query.all()

        result = []

        for doc in doctors:
            result.append({
                "doctor_id": doc.id,
                "name": doc.user.name,
                "department": doc.department.name if doc.department else None
            })

        return result
    
    @staticmethod
    def book_appointment(data):

        doctor_id = data.get("doctor_id")
        date = data.get("date")
        time = data.get("time")

        patient = Patient.query.filter_by(user_id=current_user.id).first()

        if not patient:
            return {"message": "Patient not found"}, 404

        # prevent double booking
        existing = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            time=datetime.strptime(time, "%H:%M").time(),
            status="Booked"
        ).first()

        if existing:
            return {"message": "Slot already booked"}, 400

        appointment = Appointment(
            doctor_id=doctor_id,
            patient_id=patient.id,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            time=datetime.strptime(time, "%H:%M").time(),
            status="Booked"
        )

        db.session.add(appointment)
        db.session.commit()

        return {"message": "Appointment booked"}, 201