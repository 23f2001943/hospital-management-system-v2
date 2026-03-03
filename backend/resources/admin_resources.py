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