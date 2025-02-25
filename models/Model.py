import glob
import os
import random
import sqlite3
from datetime import datetime

from models.Database import Database
from models.FileObject import FileObject
from models.Leaderboard import Leaderboard


class Model:
    def __init__(self):
        self.database = Database()
        self.__image_files = [] # Tühi list piltide jaoks
        self.load_images('images') # Anname kausta kaasa
        #self.__file_object = FileObject('databases', 'words.txt')
        #self.__categories = self.__file_object.get_unique_categories() # Unikaalsed kategooriad
        #print(self.__file_object.get_random_word('amet'))              # Näitab konsooli "amet"
        #self.__scoreboard = Leaderboard()                              # Loo edetabeli objekt (teeb vajadusel faili)
        self.__scoreboard = Database()                                  # Loo edetabeli objekt (teeb vajadusel tabeli)
        self.__categories = self.database.get_categories()              # Vali sõna kategooria andmebaasist


        # Mängu muutujad
        self.__new_word = None                   # Juhuslik arvatav sõna
        self.__user_word = []                    # Kõik kasutaja leitud tähed
        self.__counter = 0                       # Vigade loendur näit 5 viga, pilt 5
        self.__all_user_chars = []               # Tähed, mis ei sobi, valesti sisestatud

        # Tiitelriba tekst, vaheldub
        self.titles = ['Poomismäng 2025', 'Kas jäid magama', 'Ootan su käiku', 'Sisesta juba täht', 'Zzzzz....']

        #self.database.close()                    # Sulge andmebaas


    def load_images(self, folder):
        # Mängu jooksul muutuvad pildid
        if not os.path.exists(folder):          # Kui kausta pole olemas
            raise FileNotFoundError(f'Kausta {folder} ei ole.')

        images = glob.glob(os.path.join(folder,'*.png'))
        if not images:
            raise FileNotFoundError(f'Kaustas {folder} ei ole PNG laiendiga faile.')

        self.__image_files = images


    def start_new_game(self, category):
        # Uue mänguga alustamine
        if category == 0 or category == "Vali kategooria":  # Kategooriat ei valita
            category = None
        self.__new_word = self.database.get_random_word(category)
        #self.__new_word = self.database.get_random_word(category.lower())
        print({self.__new_word})                            # Juhuslik sõna, uue mängu alguses

        """ if category_id == 0:
            category = None
        # MUUDAN ALLIKAKS DATABASE
        #self.__new_word = self.__file_object.get_random_word(category) # Juhuslik sõna"""

        # Juhuslik sõna
        print(f"New word Model test- {self.__new_word}")
        self.__user_word = []               # Algseis
        self.__counter = 0                  # Algseis
        self.__all_user_chars = []          # Algseis

        # Asenda sõnas kõik tähekohad kriipsudega näit MAJA=>_ _ _ _
        for x in range(len(self.__new_word)):
            self.__user_word.append('_')
        print(self.__new_word, self.__user_word)  # Kontrollin alakriipse


    def get_user_input(self, user_input):
        # User_input on sisestuskasti kirjutatud tähed
        if user_input:
            user_char = user_input[:1]            # Esimene märk sisestusest, kui mitu, võta esimene
            if user_char.lower() in self.__new_word.lower(): # võrdleme väikseid tähti
                self.change_user_input(user_char) # Leiti täht
            else:                                 # Ei leitud tähte
                self.__counter += 1               # Valetäht listi ja suureks, counter loendab valesid tähti
                self.__all_user_chars.append(user_char.upper())
        else:                                     # Kasutaja ei sisestanud midagi
            self.__counter += 1



    def change_user_input(self, user_char):
        # Teeme sõna listiks, et tähti eraldi kontrollida
        current_word = self.char_to_list(self.__new_word)  # Listi kujul ära arvatav sõna
        x = 0
        for c in current_word:                             # Üks täht listist, kollasel taustal
            if c.lower() == user_char.lower():
                self.__user_word[x] = user_char.upper()
            x += 1

    @staticmethod
    def char_to_list(word):
        # String to List "test" sellest tuleb = ['t', 'e', 's', 't']
        chars = []
        chars[:0] = word
        return chars


    def get_all_user_chars(self):
        return ', '.join(self.__all_user_chars) # list tehakse komaga eraldatud stringiks # t, e, s, t

    def save_player_score(self, name, seconds):
        self.database = Database()
        today = datetime.now().strftime('%Y-%m-%d %T')  # Hetke kuupäev-aeg
        if not name.strip():
            name = random.choice(['Teadmata', 'Tundmatu', 'Unknown'])  # Kui nime ei sisestata
        #print(f"Salvestamine - self.database: {self.database}, type: {type(self.database)}")  # Test

        if self.database.cursor:
            try:
                sql = f'INSERT INTO leaderboard (name, word, letters, game_length, game_time) VALUES ("{name}","{self.__new_word}","{self.get_all_user_chars()}","{seconds}","{today}")'
                self.database.cursor.execute(sql)
                self.database.conn.commit()
                print(f"Salvestamine... = {sql}")  # Test

            except sqlite3.Error as error:
                print(f"Viga! {error}")
            finally:
                print("Mängija lisati edetabelisse.")


    # GETTTERS
    @property
    def image_files(self):
        """Tagastab piltide listi"""
        return self.__image_files
    @property
    def categories(self):
        """ Taghastaba kategooriate listi"""
        return self.__categories

    @property
    def user_word(self):
        """ Tagastab kasutaja leitud tähed""" # õiged tähed, mis sobivad sõnaga
        return self.__user_word

    @property
    def counter(self):
        """ Tagastab vigade arvu"""
        return self.__counter

