from flask import Blueprint, jsonify, request
from app.controllers.project_controller import ProjectController

project_bp = Blueprint('project', __name__)
project_controller = ProjectController()

@project_bp.route('/project/initialize', methods=['POST'])
def initialize_project():
    """
    Initialize a new project
    """
    data = request.get_json()
    result = project_controller.initialize_project(data)
    return jsonify(result)

@project_bp.route('/project/<project_id>/configure', methods=['POST'])
def configure_project(project_id):
    """
    Configure project details
    """
    data = request.get_json()
    result = project_controller.configure_project(project_id, data)
    return jsonify(result)

@project_bp.route('/project/<project_id>/assign/<manager_id>', methods=['POST'])
def assign_manager(project_id, manager_id):
    """
    Assign manager to project
    """
    result = project_controller.assign_manager(project_id, manager_id)
    return jsonify(result)