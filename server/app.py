#!/usr/bin/env python3
import os
from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from server.models import db, Restaurant, RestaurantPizza, Pizza 


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)



@app.route("/")
def index():
    return "<h1>Code Challenge: Pizza Restaurants 🍕</h1>"


# GET /restaurants
class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict(only=("id", "name", "address")) for r in restaurants], 200


# GET /restaurants/<id>, DELETE /restaurants/<id>
class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return restaurant.to_dict(), 200

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204


# GET /pizzas
class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict(only=("id", "name", "ingredients")) for p in pizzas], 200


# POST /restaurant_pizzas
class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_rp = RestaurantPizza(
                price=data["price"],
                pizza_id=data["pizza_id"],
                restaurant_id=data["restaurant_id"],
            )
            db.session.add(new_rp)
            db.session.commit()
            return new_rp.to_dict(), 201
        except Exception:
            return {"errors": ["validation errors"]}, 400



api.add_resource(Restaurants, "/restaurants")
api.add_resource(RestaurantById, "/restaurants/<int:id>")
api.add_resource(Pizzas, "/pizzas")
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")



if __name__ == "__main__":
    app.run(port=5555, debug=True)
