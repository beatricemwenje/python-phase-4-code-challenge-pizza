#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    print("Deleting data...")

    # ✅ delete association table first to avoid foreign key errors
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='address1')
    bistro = Restaurant(name="Sanjay's Pizza", address='address2')
    palace = Restaurant(name="Kiki's Pizza", address='address3')
    restaurants = [shack, bistro, palace]

    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(
        name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(
        name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    print("Creating RestaurantPizzas...")
    pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=1)
    pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=4)
    pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=5)
    restaurant_pizzas = [pr1, pr2, pr3]

    db.session.add_all(restaurants + pizzas + restaurant_pizzas)
    db.session.commit()

    print("Seeding done!")
