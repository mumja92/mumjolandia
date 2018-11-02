# from src.modules.food.food_database_supervisor import FoodDatabaseSupervisor
#
# f = FoodDatabaseSupervisor('data/jedzonko2.db')
# print(f.select_meal_ingradients())
# print(f.insert_ingradient('xDD'))
# print(f.insert_meal(1, 'xD', 'xDD'))
# print(f.insert_meal_ingradient(1, 2, 2, 10))
import os

print(os.path.isdir("data2"))
try:
    os.mkdir("data")
except OSError as e:
    print(str(e))
