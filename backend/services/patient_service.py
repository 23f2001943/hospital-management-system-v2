from models import Patient
from extensions import db
from flask_security import current_user


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