# db browser for sqlite
from src.modules.food.food_database_supervisor import FoodDatabaseSupervisor

f = FoodDatabaseSupervisor('data/jedzonko2.db')
dish = f.select_meal_ingredients(2)
print(dish[0][0])
for t in dish:
    print(t[1] + ' - ' + str(t[3]) + ' [' + t[2].rstrip() + ']')

# print(f.insert_ingradient('xDD'))
# print(f.insert_meal(1, 'xD', 'xDD'))
# print(f.insert_meal_ingradient(1, 2, 2, 10))