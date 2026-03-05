from flask import Blueprint, request, jsonify
from flask_security import auth_required
from flask_security.decorators import roles_required
from services.admin_service import AdminService

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/add-doctor", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def add_doctor():
    data = request.get_json()
    response, status = AdminService.add_doctor(data)
    return jsonify(response), status

@admin_bp.route("/dashboard/stats", methods=["GET"])
@auth_required("token")
@roles_required("admin")
def admin_dashboard_stats():
    stats = AdminService.get_dashboard_stats()
    return jsonify(stats), 200


@admin_bp.route("/doctors", methods=["GET"])
@auth_required("token")
@roles_required("admin")
def get_doctors():
    name = request.args.get("name")
    specialization = request.args.get("specialization")

    doctors = AdminService.get_doctors(name, specialization)

    return jsonify(doctors), 200

@admin_bp.route("/update-doctor/<int:doctor_id>", methods=["PUT"])
@auth_required("token")
@roles_required("admin")
def update_doctor(doctor_id):
    data = request.get_json()
    response, status = AdminService.update_doctor(doctor_id, data)
    return jsonify(response), status


@admin_bp.route("/blacklist-doctor/<int:doctor_id>", methods=["PATCH"])
@auth_required("token")
@roles_required("admin")
def blacklist_doctor(doctor_id):
    response, status = AdminService.blacklist_doctor(doctor_id)
    return jsonify(response), status

@admin_bp.route("/departments", methods=["GET"])
@auth_required("token")
@roles_required("admin")
def get_departments():
    departments = AdminService.get_departments()
    return jsonify(departments), 200

@admin_bp.route("/delete-doctor/<int:doctor_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("admin")
def delete_doctor(doctor_id):
    response, status = AdminService.delete_doctor(doctor_id)
    return jsonify(response), status