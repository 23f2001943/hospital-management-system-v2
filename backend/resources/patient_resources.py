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