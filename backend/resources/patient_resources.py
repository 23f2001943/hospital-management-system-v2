from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required
from services.patient_service import PatientService

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

    return doctor.availability or [], 200

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