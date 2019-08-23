import logging
import sqlite3
from pathlib import Path

from src.modules.game.game_factory import GameFactory


class GameDbAdapter:
    def __init__(self, db_location='data/games.db'):
        self.db_location = db_location
        self.__init_database()

    def add_game(self, game):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO game (name) VALUES (?)', (game.name, ))
        except (sqlite3.IntegrityError, sqlite3.DatabaseError) as e:
            logging.info('sqlite error: ' + e.args[0])
            return False
        finally:
            conn.commit()
            c.close()
        return True

    def get_games(self):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        try:
            c.execute('''SELECT * FROM game''')
            games = c.fetchall()
        except (sqlite3.IntegrityError, sqlite3.OperationalError, sqlite3.DatabaseError) as e:
            logging.info('sqlite error: ' + e.args[0])
            return None
        c.close()
        return_value = []
        for g in games:
            return_value.append(GameFactory().get_game(g[1], g[0]))
        return return_value

    def remove_game(self, game):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        return_value = 0
        try:
            c.execute('''DELETE FROM game WHERE game_id = ''' + str(game.game_id))
            conn.commit()
            return_value = c.rowcount
        except sqlite3.DatabaseError as e:
            logging.info('sqlite error: ' + e.args[0])
            return_value = 0
        finally:
            c.close()
            return return_value

    def __create_new_db(self):
        conn = sqlite3.connect(self.db_location)
        c = conn.cursor()
        c.execute('''CREATE TABLE game
                     (game_id INTEGER PRIMARY KEY,
                     name varchar(50) NOT NULL UNIQUE)''')
        conn.commit()
        c.close()

    def __init_database(self):
        file = Path(self.db_location)
        if not file.is_file():
            logging.info('Creating new database')
            self.__create_new_db()
        else:
            conn = sqlite3.connect(self.db_location)
            c = conn.cursor()
            try:
                c.execute('''SELECT * FROM game''')
            except sqlite3.DatabaseError as e:
                logging.error('''Database exists but is incorrect! Try to recover data manually and delete old file when done''')
            finally:
                conn.close()
