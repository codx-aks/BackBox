from flask import Blueprint, jsonify, request, Response
from app.controllers.cctv_controller import CCTVController

cctv_bp = Blueprint('cctv', __name__)
cctv_controller = CCTVController()

@cctv_bp.route('/cctv/<cctv_name>/livefeed', methods=['GET'])
def get_livefeed(cctv_name):
    """
    Stream video feed for a specific CCTV by name (e.g., CCTV1, CCTV2)
    """
    return cctv_controller.get_livefeed(cctv_name)

@cctv_bp.route('/cctvs', methods=['GET'])
def get_all_cctvs():
    result = cctv_controller.get_all_cctvs()
    return jsonify(result)

@cctv_bp.route('/cctvs/floor/<floor>', methods=['GET'])
def get_cctvs_by_floor(floor):
    result = cctv_controller.get_cctvs_by_floor(floor)
    return jsonify(result)

@cctv_bp.route('/cctv/<watchid>', methods=['GET'])
def get_cctv_by_watchid(watchid):
    result = cctv_controller.get_cctv_by_watchid(watchid)
    return jsonify(result)
