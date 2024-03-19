from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Sneaker, sneaker_schema, sneakers_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/sneakers', methods = ['POST'])
@token_required
def create_sneaker(current_user_token):
    brand = request.json['brand']
    sneaker_name = request.json['sneaker_name']
    athletic_style = request.json['athletic_style']
    lining_material = request.json['lining_material']
    season = request.json['season']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    sneaker = Sneaker(brand, sneaker_name, athletic_style, lining_material, season, user_token = user_token )

    db.session.add(sneaker)
    db.session.commit()

    response = sneaker_schema.dump(sneaker)
    return jsonify(response)

#Read All
@api.route('/sneakers', methods=['GET'])
@token_required
def get_sneakers(current_user_token):
    a_user = current_user_token.token
    sneakers = Sneaker.query.filter_by(user_token = a_user).all()
    response = sneakers_schema.dump(sneakers)

    return jsonify(response)

#Read One
@api.route('/sneakers/<id>', methods=['GET'])
@token_required
def get_sneaker(current_user_token,id):
    sneaker = Sneaker.query.get(id)
    response = sneaker_schema.dump(sneaker)
    return jsonify(response)

#Update
@api.route('/sneakers/<id>', methods = ['POST','PUT'])
@token_required
def update_sneaker(current_user_token, id):
    sneaker = Sneaker.query.get(id)
    sneaker.brand = request.json['brand']
    sneaker.sneaker_name = request.json['sneaker_name']
    sneaker.athletic_style = request.json['athletic_style']
    sneaker.lining_material = request.json['lining_material']
    sneaker.season = request.json['season']
    sneaker.user_token = current_user_token.token

    db.session.commit()
    response = sneaker_schema.dump(sneaker)
    return jsonify(response)

#Delete 
@api.route('/sneakers/<id>', methods =['DELETE'])
@token_required
def delete_sneaker(current_user_token, id):
    sneaker = Sneaker.query.get(id)
    db.session.delete(sneaker)
    db.session.commit()
    response = sneaker_schema.dump(sneaker)
    return jsonify(response)