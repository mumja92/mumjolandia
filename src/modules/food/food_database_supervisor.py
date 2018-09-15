import sqlite3


class FoodDatabaseSupervisor:
    def __init__(self, db_location):
        self.db_location = db_location
        con = sqlite3.connect('file:data/jedzonko22.db?mode=rw', uri=True)
        con.close()

    def select_meal_ingradients(self):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        c.execute("select * from meal_ingradients")
        return_values = c.fetchall()
        conn.close()
        return return_values


    def insert_ingradient(self, name):
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

    def insert_meal_ingradient(self, meal_id, ingradient_id, amount_type, amount):
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
