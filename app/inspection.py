from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (create_inspection, get_inspection_by_id, update_inspection_status, get_inspections_by_user)
from .utils import validate_image_url
import logging

inspection_bp = Blueprint('inspection', __name__, url_prefix='/inspection')

@inspection_bp.route('', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    vehicle_number = data.get('vehicle_number')
    damage_report = data.get('damage_report')
    image_url = data.get('image_url')
    if not (vehicle_number and damage_report and image_url):
        return jsonify({'error': 'Required fields missing'}), 400
    if not validate_image_url(image_url):
        return jsonify({'error': 'Invalid image URL'}), 400
    user_id = int(get_jwt_identity())
    try:
        inspection_id = create_inspection(vehicle_number, user_id, damage_report, image_url)
        return jsonify({'inspection_id': inspection_id}), 201
    except Exception as e:
        logging.error(f"DB Error: {e}")
        return jsonify({'error': 'database error'}), 500

@inspection_bp.route('/<int:inspection_id>', methods=['GET'])
@jwt_required()
def get_inspection(inspection_id):
    user_id = int(get_jwt_identity())
    inspection = get_inspection_by_id(inspection_id)
    if not inspection or inspection.inspected_by != user_id:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({
        'id': inspection.id,
        'vehicle_number': inspection.vehicle_number,
        'damage_report': inspection.damage_report,
        'status': inspection.status,
        'image_url': inspection.image_url,
        'created_at': inspection.created_at.isoformat()
    }), 200

@inspection_bp.route('/<int:inspection_id>', methods=['PATCH'])
@jwt_required()
def update_status(inspection_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    status = data.get('status')
    if status not in ['reviewed', 'completed']:
        return jsonify({'error': 'Invalid status, please update as reviewed or completed'}), 400
    updated = update_inspection_status(inspection_id, status, user_id)
    if not updated:
        return jsonify({'error': 'not found'}), 404
    return jsonify({'message': 'Status updated'}), 200

@inspection_bp.route('', methods=['GET'])
@jwt_required()
def list_inspections():
    user_id = int(get_jwt_identity())
    status = request.args.get('status')
    inspections = get_inspections_by_user(user_id, status)
    return jsonify(inspections), 200