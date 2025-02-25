import os
import sqlite3
import sys
from models.Timer import Timer

class Database:
    db_name = "databases/hangman_2025.db"
    table_leaderboard = "leaderboard"
    table_words = "words"

    def __init__(self):
        """ Kontolli andmebaasi olemasolu """
        if not os.path.exists(self.db_name):
            raise FileNotFoundError(f"Andmebaasi '{self.db_name}' ei leitud")

        """Konstruktor"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = None
        self.connect()  # Loo ühendus
        self.cursor = self.conn.cursor()
        self.check_if_table_exists()
        self.create_table_leaderboard()
        self.get_leaderboard()
        self.get_categories()
        self.get_random_word()


    def check_if_table_exists(self):
        """Kontolli kas tabelid on andmebaasis olemas """
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tabelid = {row[0] for row in self.cursor.fetchall()}

            # Mõlemad tabelid on puudu.
            if self.table_words not in tabelid and self.table_leaderboard not in tabelid:
                print(f"Viga! Tabeleid '{self.table_words}' ja '{self.table_leaderboard}' ei leitud. Programm lõpetab töö.")
                sys.exit(1)    # Veaga lõpetamine

            # 'Leaderboard' on puudu, tehaks uus tabel.
            if self.table_words in tabelid and self.table_leaderboard not in tabelid:
                print(f"Tabel '{self.table_words}' on, aga '{self.table_leaderboard}' pole.")
                self.create_table_leaderboard()
                print(f"Loodi uus tabel '{self.table_leaderboard}'")
                return

            # 'Words' on puudu. Programm sulgub.
            if self.table_leaderboard in tabelid and self.table_words not in tabelid:
                print(f"Viga! Tabelit '{self.table_words}'ei leitud. Programm lõpetab töö.")
                sys.exit(1)   # Veaga lõpetamine

            # Mõlemad tabelid on olemas
            print(f"Mõlemad tabelid on olemas.")

        except sqlite3.Error as error:
            print(f"Viga! {error}")
            raise


    def create_table_leaderboard(self):
        """ Kui tabel leaderboard puudub"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                word TEXT NOT NULL,
                letters TEXT,
                game_length INTEGER NOT NULL,
                game_time TEXT NOT NULL
            )
        ''')
        #print(f'Loodi tabel: {self.table_leaderboard}.')
        self.conn.commit()


    def connect(self):
        """Loob ühenduse andmebaasiga"""
        try:
            if self.conn:
                self.conn.close()  # eelnev ühendus suletakse
                print('Varasem andmebaasi ühendus suleti')
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Uus ühendus andmebaasiga {self.db_name} loodud')
        except sqlite3.Error as error:
            print(f'Tõrge andmebaasi ühenduse loomisel:{error}')
            self.conn = None
            self.cursor = None


    def get_random_word(self, category=None):
        """ Vali juhuslik sõna kategooriaga või ilma"""
        try:
            if category is None:  # Kategooriat ei valita
                self.cursor.execute("SELECT word FROM words ORDER BY RANDOM() LIMIT 1")
            else:                 # Kategooria valitakse
                category = category.lower()
                self.cursor.execute("SELECT word FROM words WHERE category = ? ORDER BY RANDOM() LIMIT 1", (category,))
                #self.cursor.execute("SELECT word FROM words WHERE LOWER(category) = LOWER(?) ORDER BY RANDOM() LIMIT 1", (category,))
            result = self.cursor.fetchone()
            if result:
                return str(result[0])  # Tagastatakse juhuslik sõna (esimene column)
            else:
                raise ValueError(f"Sobivaid sõnu pole: {category}" if category else "Andmebaasis sõnu pole.")
        except sqlite3.Error as error:
            print(f"Andmebaasi viga!: {error}")
            raise


    def get_categories(self):
        """Vali kategooriad"""
        self.cursor.execute("SELECT DISTINCT category FROM words")
        data = self.cursor.fetchall()
        categories = [category[0] for category in data]
        if [category[0] for category in data] == ['']:
           raise ValueError(f"Kategooria puudub.")
        categories.sort()
        categories.insert(0, 'Vali kategooria')
        print(f'Kategooriad: {categories}.')


        return [category.capitalize() for category in categories]


    def get_leaderboard(self):
        """Loe andmebaasist andmed ning järjesta mängijad:
            Kõige kiiremad eespool, järgmisena, kellel vähem valesid tähti """
        self.cursor.execute(
            "SELECT * FROM leaderboard ORDER BY game_length ASC, length(letters) ASC")
        # print(f"Siin on edetabel kiiremad eespool='{self.get_leaderboard}'")   # Test
        lb_data = self.cursor.fetchall()
        #print(lb_data)   # Test
        return lb_data


    def close(self):
        """Sulge andmebaas"""
        self.conn.close()


