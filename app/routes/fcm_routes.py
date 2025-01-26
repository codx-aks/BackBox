from flask import Blueprint, jsonify, request
from app.controllers.fcm_controller import FCMController
import firebase_admin
from firebase_admin import credentials

fcm_bp = Blueprint('fcm', __name__)
fcm_controller = FCMController()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

@fcm_bp.route('/fcm/register', methods=['POST'])
def register_device():
    # FCM registration logic here
    pass

@fcm_bp.route('/fcm/send', methods=['POST'])
def send_notification():
    response, status_code = FCMController.send_topic_notification(request.get_json())
    return jsonify(response), status_code

@fcm_bp.route('/fcm/subscribe', methods=['POST'])
def subscribe_to_topic():
    response, status_code = FCMController.subscribe_to_topic(request.get_json())
    return jsonify(response), status_code

@fcm_bp.route('/fcm/unsubscribe', methods=['POST'])
def unsubscribe_from_topic():
    response, status_code = FCMController.unsubscribe_from_topic(request.get_json())
    return jsonify(response), status_code