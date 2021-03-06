import sqlite3
import unicodedata
from pathlib import Path


class FoodDatabaseHelper:
    def __init__(self, db_location):
        self.db_location = db_location
        self.database_ok = self.is_database_ok()

    def is_database_ok(self):
        file = Path(self.db_location)
        if not file.is_file():
            return False

        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''SELECT * FROM recipe_day''')
            return_value = True
        except sqlite3.DatabaseError as e:
            return_value = False
        conn.close()
        return return_value

    def get_meal(self, meal_id):
        if not isinstance(meal_id, int):
            return None
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''SELECT * FROM MEAL WHERE id_meal = ''' + str(meal_id))
            return_value = c.fetchall()
        except sqlite3.IntegrityError as e:
            return_value = 'sqlite error: ' + e.args[0]
        conn.close()
        return return_value

    def get_meal_ingredients(self, meal_id):
        if meal_id is None:
            return None
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''
            SELECT meal.name as name, ingradient.name as 'ingradient', amount_type.name as 'amount type', amount as 'amount' 
            FROM meal_ingradients 
            INNER JOIN meal ON meal.id_meal = meal_ingradients.fk_meal_id 
            INNER JOIN ingradient ON ingradient.id_ingradient = meal_ingradients.fk_ingradient_id 
            INNER JOIN amount_type ON amount_type.id_amount_type = meal_ingradients.fk_amount_type
            WHERE meal.id_meal = 
            ''' + str(meal_id))
            return_value = c.fetchall()
        except sqlite3.IntegrityError as e:
            return_value = 'sqlite error: ' + e.args[0]
        conn.close()
        return return_value

    def get_meals(self, fk_meal_type=None):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            if isinstance(fk_meal_type, int):
                c.execute('''SELECT * FROM meal WHERE fk_meal_type = ''' + str(fk_meal_type))
            else:
                c.execute('''SELECT * FROM meal''')
            return_value = c.fetchall()
        except sqlite3.IntegrityError as e:
            return_value = 'sqlite error: ' + e.args[0]
        conn.close()
        return return_value

    def get_recipes_day(self, recipe_id):
        return_value = 0
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''SELECT * FROM recipe_day WHERE id_recipe_day = ''' + str(recipe_id))
            return_value = c.fetchall()
        except sqlite3.IntegrityError as e:
            return_value = 'sqlite error: ' + e.args[0]
        conn.close()
        return return_value

    def select_meal_ingredients(self, id_meal):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        c.execute("SELECT meal.name as name, ingradient.name as 'ingradient', amount_type.name as 'amount type', "
                  "amount as 'amount' "
                  "FROM meal_ingradients "
                  "INNER JOIN meal ON meal.id_meal = meal_ingradients.fk_meal_id "
                  "INNER JOIN ingradient ON ingradient.id_ingradient = meal_ingradients.fk_ingradient_id "
                  "INNER JOIN amount_type ON amount_type.id_amount_type = meal_ingradients.fk_amount_type "
                  "WHERE meal.id_meal = " + str(id_meal))
        return_values = c.fetchall()
        conn.close()
        return return_values

    def insert_recipe_day(self, b1, b2, d, t, s):
        return_value = 0
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO recipe_day (fk_breakfast, fk_second_breakfast, fk_dinner, fk_tea, fk_supper) VALUES (?, ?, ?, ?, ?)''', (b1, b2, d, t, s,))
        except sqlite3.IntegrityError as e:
            return_value = 'sqlite error: ' + e.args[0]  # column name is not unique
        conn.commit()
        conn.close()
        return return_value

    def insert_ingredient(self, name):
        return_value = 0
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO ingradient (name) VALUES (?)''', (name,))
        except sqlite3.IntegrityError as e:
            return_value = 'sqlite error: ' + e.args[0]
        conn.commit()
        conn.close()
        return return_value

    def insert_meal_ingredient(self, meal_id, ingradient_id, amount_type, amount):
        return_value = 0
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO meal_ingradients (fk_meal_id, fk_ingradient_id, fk_amount_type, amount) VALUES (?, ?, ?, ?)''', (meal_id, ingradient_id, amount_type, amount,))
        except sqlite3.IntegrityError as e:
            return_value = 'sqlite error: ' + e.args[0]
        conn.commit()
        conn.close()
        return return_value

    def insert_meal(self, type, name, recipe):
        return_value = 0
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            result = c.execute('''INSERT INTO meal (fk_meal_type, name, recipe) VALUES (?, ?, ?)''', (type, name, recipe,))
            return_value = result.lastrowid
        except sqlite3.IntegrityError as e:
            return_value = None
        conn.commit()
        conn.close()
        return return_value

    def get_ingredient_id(self, name):
        ingredient_id = self.__get_ingredient_id_if_exists(name)
        if ingredient_id is None:
            self.insert_ingredient(name)
            ingredient_id = self.__get_ingredient_id_if_exists(name)
        return ingredient_id

    def __normalize_text(self, text):
        temp = text
        temp = temp.replace(' ', '')
        temp = temp.replace('\n', '')
        return unicodedata.normalize("NFKD", temp.casefold())

    def __strings_equal(self, left, right):
        return self.__normalize_text(left) == self.__normalize_text(right)

    def __get_ingredient_id_if_exists(self, name):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        c.execute("SELECT * FROM ingradient")
        response = c.fetchall()
        conn.close()
        return_value = None
        for x in response:
            if self.__strings_equal(x[1], name):
                return_value = x[0]
        return return_value

    def get_meal_id_if_exists(self, name, recipe, meal_type):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        c.execute("SELECT * FROM meal")
        response = c.fetchall()
        conn.close()
        return_value = None
        for x in response:
            if self.__strings_equal(str(x[1]), str(meal_type)) and self.__strings_equal(x[2], name):
                return_value = x[0]
                break
        return return_value

    def get_new_meal_id(self, value, name, recipe):
        meal_id = self.insert_meal(value, name, recipe)
        return meal_id

    def get_recipes_ids(self):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        c.execute("SELECT * FROM recipe_day")
        response = c.fetchall()
        conn.close()
        return response

    def get_meal_recipe(self, id):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        c.execute("SELECT * FROM meal")
        response = c.fetchall()
        conn.close()
        for x in response:
            if x[0] == id:
                return x[3]
        return None

    def get_meal_type(self, id):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        c.execute("SELECT * FROM meal")
        response = c.fetchall()
        conn.close()
        for x in response:
            if x[0] == id:
                return x[1]
        return None