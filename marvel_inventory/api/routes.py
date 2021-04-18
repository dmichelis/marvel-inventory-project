from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import User, Hero, hero_schema, heroes_schema, db

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return{ 'some': 'value'}


@api.route('/heroes', methods = ['POST'])
@token_required
def create_hero(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    super_power = request.json['super_power']
    date_created = request.json['date_created']
    user_token = current_user_token.token

    hero = Hero(name,description,comics_appeared_in,super_power,date_created,user_token=user_token)

    db.session.add(hero)
    db.session.commit()

    response = hero_schema.dump(hero)
    return jsonify(response)

@api.route('/heroes', methods = ['GET'])
@token_required
def get_heroes(current_user_token):
    owner = current_user_token.token
    heroes = Hero.query.filter_by(user_token = owner).all()
    response = heroes_schema.dump(heroes)
    return jsonify(response)

@api.route('/heroes/<id>', methods = ['GET'])
@token_required
def get_hero(current_user_token, id):
    hero = Hero.query.get(id)
    response = hero_schema.dump(hero)
    return jsonify(response)

@api.route('/heroes/<id>', methods = ['POST', 'PUT'])
@token_required
def update_hero(current_user_token, id):
    hero = Hero.query.get(id)

    hero.name = request.json['name']
    hero.description = request.json['description']
    hero.comics_appeared_in = request.json['comics_appeared_in']
    hero.super_power = request.json['super_power']
    hero.date_created = request.json['date_created']
    hero.user_token = current_user_token.token

    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)


@api.route('/heroes/<id>', methods = ['DELETE'])
@token_required
def delete_hero(current_user_token, id):
    hero = Hero.query.get(id)
    db.session.delete(hero)
    db.session.commit()
    response = hero_schema.dump(hero)
    return jsonify(response)


