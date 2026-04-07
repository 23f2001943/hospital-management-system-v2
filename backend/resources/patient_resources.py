from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required
from services.patient_service import PatientService
from models import Appointment
from datetime import datetime
from flask_security import current_user
from celery.result import AsyncResult
from flask import send_file


patient_bp = Blueprint("patient", __name__, url_prefix="/api/patient")


@patient_bp.route("/profile", methods=["GET"])
@auth_required("token")
@roles_required("patient")
def get_profile():
    response, status = PatientService.get_profile()
    return jsonify(response), status


@patient_bp.route("/profile", methods=["PUT"])
@auth_required("token")
@roles_required("patient")
def update_profile():
    data = request.get_json()
    response, status = PatientService.update_profile(data)
    return jsonify(response), status

@patient_bp.route("/doctors", methods=["GET"])
@auth_required("token")
@roles_required("patient")
def get_doctors():
    name = request.args.get("name")
    specialization = request.args.get("specialization")

    from services.admin_service import AdminService

    doctors = PatientService.get_doctors(name, specialization)

    return jsonify(doctors), 200

@patient_bp.route("/doctor/<int:doctor_id>/availability", methods=["GET"])
@auth_required("token")
@roles_required("patient")
def get_availability(doctor_id):
    from models import Doctor

    doctor = Doctor.query.get(doctor_id)

    if not doctor:
        return {"message": "Doctor not found"}, 404

    
    availability = doctor.availability or []

    result = []

    for day in availability:

        date_obj = datetime.strptime(day["date"], "%Y-%m-%d").date()

        # check bookings
        morning_booked = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=date_obj,
            time=datetime.strptime("09:00", "%H:%M").time(),
            status="Booked"
        ).first() is not None

        evening_booked = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=date_obj,
            time=datetime.strptime("17:00", "%H:%M").time(),
            status="Booked"
        ).first() is not None

        result.append({
            "date": day["date"],
            "morning": day.get("morning"),
            "evening": day.get("evening"),
            "morning_booked": morning_booked,
            "evening_booked": evening_booked
        })

    return result, 200

@patient_bp.route("/book", methods=["POST"])
@auth_required("token")
@roles_required("patient")
def book_appointment():
    data = request.get_json()
    response, status = PatientService.book_appointment(data)
    return jsonify(response), status

@patient_bp.route("/appointments", methods=["GET"])
@auth_required("token")
@roles_required("patient")
def get_appointments():
    from services.patient_service import PatientService
    data = PatientService.get_appointments()
    return jsonify(data), 200

@patient_bp.route("/appointment/<int:id>/cancel", methods=["PATCH"])
@auth_required("token")
@roles_required("patient")
def cancel_appointment(id):
    response, status = PatientService.cancel_appointment(id)
    return jsonify(response), status

@patient_bp.route("/appointment/<int:id>/reschedule", methods=["PUT"])
@auth_required("token")
@roles_required("patient")
def reschedule(id):
    data = request.get_json()
    response, status = PatientService.reschedule_appointment(id, data)
    return jsonify(response), status

@patient_bp.route("/history", methods=["GET"])
@auth_required("token")
@roles_required("patient")
def history():
    data = PatientService.get_history()
    return jsonify(data), 200

@patient_bp.route("/history/completed", methods=["GET"])
@auth_required("token")
@roles_required("patient")
def completed_history():
    data = PatientService.get_completed_history()
    return jsonify(data), 200


@patient_bp.route("/export-history", methods=["POST"])
@auth_required("token")
@roles_required("patient")
def export_csv():

    from tasks.exports import export_history   

    patient_id = current_user.patient.id

    task = export_history.delay(patient_id)

    return {
        "message": "Export started",
        "task_id": task.id
    }, 200


@patient_bp.route("/export-status/<task_id>", methods=["GET"])
@auth_required("token")
@roles_required("patient")
def export_status(task_id):

    from celery_worker import celery   

    task = AsyncResult(task_id, app=celery)

    if task.state == "SUCCESS":
        return {
            "status": "completed",
            "file": task.result
        }

    return {
        "status": task.state
    }



@patient_bp.route("/download-file", methods=["GET"])
@auth_required("token")
@roles_required("patient")
def download_file():

    file_path = request.args.get("path")

    return send_file(file_path, as_attachment=True)