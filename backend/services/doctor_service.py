from models import Doctor, Appointment, Treatment, Patient
from extensions import db
from flask_security import current_user
from datetime import datetime, date
from extensions import cache

class DoctorService:

    @staticmethod
    def get_doctor():
        return Doctor.query.filter_by(user_id=current_user.id).first()

    

    @staticmethod
    def get_dashboard():

        doctor = DoctorService.get_doctor()
        today = date.today()

        appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()

        today_appts = []
        upcoming_appts = []
        past_appts = []

        for appt in appointments:

            treatment = appt.treatment 
            data = {
                "appointment_id": appt.id,
                "patient_name": appt.patient.user.name,
                "date": appt.date.strftime("%Y-%m-%d"),
                "time": appt.time.strftime("%H:%M"),
                "status": appt.status,

                "diagnosis": treatment.diagnosis if treatment else "",
                "prescription": treatment.prescription if treatment else "",
                "notes": treatment.notes if treatment else ""
            }

            if appt.date == today:
                today_appts.append(data)

            elif appt.date > today:
                upcoming_appts.append(data)

            else:
                past_appts.append(data)

        return {
            "doctor_name": doctor.user.name, 
            "today": today_appts,
            "upcoming": upcoming_appts,
            "past": past_appts
        }

    @staticmethod
    def get_appointments(status=None):

        doctor = DoctorService.get_doctor()

        query = Appointment.query.filter_by(doctor_id=doctor.id)

        if status:
            query = query.filter(Appointment.status == status)

        appointments = query.all()

        result = []

        for appt in appointments:
            result.append({
                "appointment_id": appt.id,
                "patient_id": appt.patient_id,
                "patient_name": appt.patient.user.name,
                "date": appt.date.strftime("%Y-%m-%d"),
                "time": appt.time.strftime("%H:%M"),
                "status": appt.status
            })

        return result

    @staticmethod
    def update_appointment_status(appointment_id, status):

        doctor = DoctorService.get_doctor()

        appointment = Appointment.query.filter_by(
            id=appointment_id,
            doctor_id=doctor.id
        ).first()

        if not appointment:
            return {"message": "Appointment not found"}, 404

        if status not in ["Cancelled"]:
            return {"message": "Only cancellation allowed"}, 400

        appointment.status = status
        db.session.commit()

        cache.clear()

        return {"message": "Status updated"}, 200
    
    @staticmethod
    def add_treatment(appointment_id, data):

        doctor = DoctorService.get_doctor()

        appointment = Appointment.query.filter_by(
            id=appointment_id,
            doctor_id=doctor.id
        ).first()

        if not appointment:
            return {"message": "Appointment not found"}, 404
        
        if appointment.status == "Cancelled":
            return {"message": "Cannot treat cancelled appointment"}, 400

        # prevent duplicate treatment
        if appointment.treatment:
            return {"message": "Treatment already exists"}, 400

        diagnosis = data.get("diagnosis")
        prescription = data.get("prescription")
        notes = data.get("notes")

        treatment = Treatment(
            appointment_id=appointment.id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes
        )

        db.session.add(treatment)

        

        # optional but recommended
        appointment.status = "Completed"

        db.session.commit()

        cache.clear()

        return {"message": "Treatment added successfully"}, 201
    
    @staticmethod
    def get_patient_history(patient_id):

        appointments = Appointment.query.filter_by(
            patient_id=patient_id
        ).order_by(
            Appointment.date.desc(),
            Appointment.time.desc()
        ).all()

        result = []

        for appt in appointments:

            treatment = appt.treatment

            result.append({
                "appointment_id": appt.id,
                "date": appt.date.strftime("%Y-%m-%d") if appt.date else None,
                "time": appt.time.strftime("%H:%M") if appt.time else None,
                "status": appt.status,

                "doctor_name": appt.doctor.user.name if appt.doctor and appt.doctor.user else "-",
                "department": appt.doctor.department.name if appt.doctor and appt.doctor.department else "-",

                "diagnosis": treatment.diagnosis if treatment else None,
                "prescription": treatment.prescription if treatment else None,
                "notes": treatment.notes if treatment else None
            })

        return result
        
    @staticmethod
    def update_availability(data):

        doctor = DoctorService.get_doctor()

        availability = data.get("availability")

        if not availability:
            return {"message": "Availability required"}, 400

        doctor.availability = availability

        db.session.commit()

        cache.clear()

        return {"message": "Availability updated"}, 200
    
    @staticmethod
    def get_my_patients():

        doctor = DoctorService.get_doctor()

        appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()

        patient_map = {}

        for appt in appointments:
            p = appt.patient

            if p.id not in patient_map:
                patient_map[p.id] = {
                    "patient_id": p.id,
                    "name": p.user.name,
                    "email": p.user.email,
                    "contact": p.contact_number,
                    "statuses": []
                }

            patient_map[p.id]["statuses"].append(appt.status)

        assigned = []
        past = []

        for p in patient_map.values():

            if "Booked" in p["statuses"]:
                assigned.append({
                    "patient_id": p["patient_id"],
                    "name": p["name"],
                    "email": p["email"],
                    "contact": p["contact"]
                })
            else:
                past.append({
                    "patient_id": p["patient_id"],
                    "name": p["name"],
                    "email": p["email"],
                    "contact": p["contact"]
                })

        return {
            "assigned": assigned,
            "past": past
        }