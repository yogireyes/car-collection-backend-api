from flask import Blueprint, request, jsonify
from src.helpers import token_required
from src.models import db, CarCollection, car_schema, cars_schema
from flask_cors import cross_origin

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/health-check')
def health_check_view():
    return {'success': 'API is live'}

@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    cars = current_user_token.cars
    return jsonify(cars_schema.dump(cars))

@api.route('/cars/<string:id>', methods=['GET'])
@token_required
def get_car(current_user_token,id):
    car = CarCollection.query.filter_by(id=id,user_id=current_user_token.id).first()
    if car:
        return jsonify(car_schema.dump(car))
    else:
        return jsonify({"error":"car doesn't exist with the id provided"}), 404

@api.route('/cars', methods=['POST'])
@cross_origin(supports_credentials=True)
@token_required
def add_car(current_user_token):
    data = request.json
    if 'brand' not in data:
        return jsonify({"error":"provide brand field"}), 400
    if 'model' not in data:
        return jsonify({"error":"provide model field"}), 400
    if 'year' not in data:
        return jsonify({"error":"provide year field"}), 400
    new_car = CarCollection(brand=data['brand'], model=data['model'], year=data['year'],user_id=current_user_token.id)
    db.session.add(new_car)
    db.session.commit()
    return jsonify(car_schema.dump(new_car))

@api.route('/cars/<string:id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
@token_required
def update_car(current_user_token,id):
    car = CarCollection.query.filter_by(id=id,user_id=current_user_token.id).first()
    if car:
        data = request.json
        if 'brand' in data:
            car.brand = data['brand']
        if 'model' in data:
            car.model = data['model']
        if 'year' in data:
            car.year = data['year']
        db.session.commit()
        return jsonify(car_schema.dump(car))
    else:
        return jsonify({"error":"car doesn't exist with the id provided"}), 404

@api.route('/cars/<string:id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
@token_required
def delete_car(current_user_token,id):
    car = CarCollection.query.filter_by(id=id,user_id=current_user_token.id).first()
    if car:
        db.session.delete(car)
        db.session.commit()
        # return jsonify({'message': 'Car deleted successfully'})
        return  ('', 204)
    else:
        return jsonify({"error":"car doesn't exist with the id provided"}), 404
