from flask import Blueprint, jsonify, request

from app.controllers.alert_controller import AlertController
from app.controllers.manager_controller import ManagerController
alert_bp = Blueprint('alert', __name__)
alert_controller = AlertController()

@alert_bp.route('/all-alerts', methods=['GET'])
def get_all_alerts():
    """
    Get a list of all alerts.
    """
    result = alert_controller.get_all_alerts()
    return jsonify(result)

@alert_bp.route('/add-alert', methods=['POST'])
def add_alert():
    """
    Add a new alert to the database.
    Expects a JSON payload with alert details.
    """
    alert_data = request.get_json()
    result = alert_controller.add_alert(alert_data)
    return jsonify(result), 201
