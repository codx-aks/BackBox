from flask import Blueprint, jsonify, request
from app.controllers.worker_controller import WorkerController

worker_bp = Blueprint('worker', __name__)
worker_controller = WorkerController()

@worker_bp.route('/worker/create', methods=['POST'])
def create_worker():
    data = request.get_json()
    result = worker_controller.create_worker(data)
    return jsonify(result)

@worker_bp.route('/workers', methods=['GET'])
def get_workers():
    result = worker_controller.get_all_workers()
    return jsonify(result)

@worker_bp.route('/worker/<watch_id>', methods=['GET'])
def get_worker_by_watch_id(watch_id):
    result = worker_controller.get_worker_by_watch_id(watch_id)
    return jsonify(result)

@worker_bp.route('/updateWorker', methods=['POST'])
def update_worker_data():
    """
    Update worker's location, heart rate, and elevation
    """
    data = request.get_json()
    result = worker_controller.update_worker_data(data)
    return jsonify(result)