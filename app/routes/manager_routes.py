from flask import Blueprint, jsonify, request
from app.controllers.manager_controller import ManagerController

manager_bp = Blueprint('manager', __name__)
manager_controller = ManagerController()

@manager_bp.route('/manager/create', methods=['POST'])
def create_manager():
    data = request.get_json()
    result = manager_controller.create_manager(data)
    return jsonify(result)

@manager_bp.route('/manager/<manager_id>/project', methods=['GET'])
def get_manager_project(manager_id):
    result = manager_controller.get_manager_project(manager_id)
    return jsonify(result)