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
    
    @staticmethod
    def get_appointments():

        from models import Appointment
        from datetime import date

        patient = Patient.query.filter_by(user_id=current_user.id).first()

        if not patient:
            return []

        appointments = Appointment.query.filter_by(
            patient_id=patient.id
        ).all()

        result = []

        for appt in appointments:

            result.append({
                "appointment_id": appt.id,
                "doctor_name": appt.doctor.user.name,
                "department": appt.doctor.department.name if appt.doctor.department else None,
                "date": appt.date.strftime("%Y-%m-%d"),
                "time": appt.time.strftime("%H:%M"),
                "status": appt.status,
                "doctor_id": appt.doctor_id
            })

        return result
    
    @staticmethod
    def cancel_appointment(appointment_id):

        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return {"message": "Not found"}, 404

        appointment.status = "Cancelled"
        db.session.commit()

        return {"message": "Cancelled"}, 200
    
    @staticmethod
    def reschedule_appointment(appointment_id, data):

        appointment = Appointment.query.get(appointment_id)

        if not appointment:
            return {"message": "Not found"}, 404

        new_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        new_time = datetime.strptime(data["time"], "%H:%M").time()

        # conflict check
        existing = Appointment.query.filter_by(
            doctor_id=appointment.doctor_id,
            date=new_date,
            time=new_time,
            status="Booked"
        ).first()

        if existing:
            return {"message": "Slot already booked"}, 400

        appointment.date = new_date
        appointment.time = new_time

        db.session.commit()

        return {"message": "Rescheduled"}, 200
    
    @staticmethod
    def get_history():

        from datetime import date

        patient = Patient.query.filter_by(user_id=current_user.id).first()

        if not patient:
            return []

        appointments = Appointment.query.filter_by(
            patient_id=patient.id
        ).all()

        result = []

        for appt in appointments:

            # only past OR completed
            if appt.date >= date.today():
                continue

            result.append({
                "doctor_name": appt.doctor.user.name,
                "department": appt.doctor.department.name if appt.doctor.department else None,
                "date": appt.date.strftime("%Y-%m-%d"),
                "time": appt.time.strftime("%H:%M"),
                "status": appt.status,
                "diagnosis": appt.treatment.diagnosis if appt.treatment else None,
                "prescription": appt.treatment.prescription if appt.treatment else None,
                "notes": appt.treatment.notes if appt.treatment else None
            })

        return result
    
    @staticmethod
    def get_completed_history():

        patient = Patient.query.filter_by(user_id=current_user.id).first()

        if not patient:
            return []

        appointments = Appointment.query.filter_by(
            patient_id=patient.id,
            status="Completed"
        ).all()

        result = []

        for appt in appointments:
            result.append({
                "doctor_name": appt.doctor.user.name,
                "date": appt.date.strftime("%Y-%m-%d"),
                "time": appt.time.strftime("%H:%M"),
                "diagnosis": appt.treatment.diagnosis if appt.treatment else None,
                "prescription": appt.treatment.prescription if appt.treatment else None,
                "notes": appt.treatment.notes if appt.treatment else None
            })

        return result