import sqlite3


class FoodDatabaseSupervisor:
    def __init__(self, db_location):
        self.db_location = db_location

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

    def insert_ingredient(self, name):
        return_value = 0
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO ingradient (name) VALUES (?)''', (name,))
        except sqlite3.IntegrityError as e:
            return_value = 'sqlite error: ' + e.args[0]  # column name is not unique
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
            return_value = 'sqlite error: ' + e.args[0]  # column name is not unique
        conn.commit()
        conn.close()
        return return_value

    def insert_meal(self, type, name, recipe):
        return_value = 0
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO meal (fk_meal_type, name, recipe) VALUES (?, ?, ?)''', (type, name, recipe,))
        except sqlite3.IntegrityError as e:
            return_value = 'sqlite error: ' + e.args[0]  # column name is not unique
        conn.commit()
        conn.close()
        return return_value
