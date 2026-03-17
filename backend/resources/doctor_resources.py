from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required
from services.doctor_service import DoctorService

doctor_bp = Blueprint("doctor", __name__, url_prefix="/api/doctor")


@doctor_bp.route("/dashboard", methods=["GET"])
@auth_required("token")
@roles_required("doctor")
def dashboard():
    data = DoctorService.get_dashboard()
    return jsonify(data), 200


@doctor_bp.route("/appointments", methods=["GET"])
@auth_required("token")
@roles_required("doctor")
def get_appointments():
    status = request.args.get("status")
    data = DoctorService.get_appointments(status)
    return jsonify(data), 200


@doctor_bp.route("/appointment/<int:appointment_id>/status", methods=["PATCH"])
@auth_required("token")
@roles_required("doctor")
def update_status(appointment_id):
    data = request.get_json()
    status = data.get("status")

    response, code = DoctorService.update_appointment_status(appointment_id, status)
    return jsonify(response), code

@doctor_bp.route("/appointment/<int:appointment_id>/treatment", methods=["POST"])
@auth_required("token")
@roles_required("doctor")
def add_treatment(appointment_id):
    data = request.get_json()
    response, code = DoctorService.add_treatment(appointment_id, data)
    return jsonify(response), code


@doctor_bp.route("/patient/<int:patient_id>/history", methods=["GET"])
@auth_required("token")
@roles_required("doctor")
def patient_history(patient_id):
    data = DoctorService.get_patient_history(patient_id)
    return jsonify(data), 200


@doctor_bp.route("/availability", methods=["PUT"])
@auth_required("token")
@roles_required("doctor")
def update_availability():
    data = request.get_json()
    response, code = DoctorService.update_availability(data)
    return jsonify(response), code

@doctor_bp.route("/patients", methods=["GET"])
@auth_required("token")
@roles_required("doctor")
def get_my_patients():
    data = DoctorService.get_my_patients()
    return jsonify(data), 200