from flask import Blueprint, request, jsonify
from src.helpers import token_required
from src.models import db, CarCollection, car_schema, cars_schema,User
from flask_cors import cross_origin

api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/health-check')
def health_check_view():
    return {'success': 'API is live'}


@api.route('/signup', methods=['POST'])
def api_signup():
    data = request.json
    first_name = data.get('first_name',None)
    last_name = data.get('last_name',None)
    email = data.get('email',None)
    password = data.get('password',None)
    
    if not first_name or not last_name or not email or not password:
        return jsonify({"error":"email, first_name, last_name,password is required"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error":"Email already registered.Choose a another email address"}), 400
    
    user = User(first_name=first_name, last_name=last_name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    response = {
        'message': 'User successfully created.',
        'email': email
    }

    return jsonify(response), 201



@api.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def api_login():
    data = request.json

    email = data.get('email',None)
    password = data.get('password',None)
    
    if not email or not password:
        return jsonify({"error":"email,password is required"}), 400

    user = User.query.filter(User.email == email).first()

    if user and user.check_password(password):
        token = user.token
        response = {
            'message': 'Successfully logged in.',
            'token': token
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Invalid credentials. Please try again.'
        }
        return jsonify(response), 401


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
