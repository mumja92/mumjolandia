import sqlite3

from src.modules.food.food_database_supervisor import FoodDatabaseSupervisor
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor

MumjolandiaSupervisor().run_cli()

# f = FoodDatabaseSupervisor('data/jedzonko2.db')
# print(f.select_meal_ingradients())
# print(f.insert_ingradient('xDD'))
# print(f.insert_meal(1, 'xD', 'xDD'))
# print(f.insert_meal_ingradient(1, 2, 2, 10))
