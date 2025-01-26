from flask import Blueprint, jsonify, request
from app.controllers.test_controller import TestController

test_bp = Blueprint('test', __name__)
test_controller = TestController()

@test_bp.route('/test-connection', methods=['GET'])
def test_connection():
    result = test_controller.test_db_connection()
    return jsonify(result)

@test_bp.route('/test', methods=['POST'])
def create_test_document():
    data = request.get_json()
    result = test_controller.create_test_document(data)
    return jsonify(result)

@test_bp.route('/test', methods=['GET'])
def get_all_documents():
    result = test_controller.get_all_documents()
    return jsonify(result)