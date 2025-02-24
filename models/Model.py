import glob
import os
import random
from datetime import datetime

from models.FileObject import FileObject
from models.Leaderboard import Leaderboard


class Model:
    def __init__(self):
        self.__image_files = [] # Tühi list piltide jaoks
        self.load_images('images') # Anname kausta kaasa
        self.__file_object = FileObject('databases', 'words.txt')
        self.__categories = self.__file_object.get_unique_categories() #Unikaalsed kategooriad
        #print(self.__file_object.get_random_word('amet')) # Näitab konsooli "amet"
        self.__scoreboard = Leaderboard() #Loo edetabeli objekt (teeb vajadusel faili)
        self.titles = ['Poomismäng 2025', 'Kas jäid magama?', 'Ma ootan su käiku!', 'Sisesta juba see täht!', 'Äratus linnuke!', 'Sa kaotad!'] #List sõnumitega, mdia kuvatakse aknas mängu ajal iga 5 sek tagant

        # Mängu muutujad
        self.__new_word = None #Juhuslik sõna mängu jaoks. Sõna mida tuleb ära arvata
        self.__user_word = [] # Kõik kasutaja leitud tähed (visuaal)
        self.__counter = 0 #Vigade loendur - sellest sõltub ka milline pilt näidata
        self.__all_user_chars = [] # Kõik valesti sisestatud tähed


    def load_images(self, folder):
        if not os.path.exists(folder):
            raise FileNotFoundError(f'Kausta {folder} ei ole.') #veateaede kui kausta pole
        images = glob.glob(os.path.join(folder, '*.png'))
        if not images:
            raise FileNotFoundError(f'Kausta {folder} ei ole PNG laiendiga faile.')

        self.__image_files = images


    def start_new_game(self, category_id, category):
        if category_id == 0:
            category = None

        self.__new_word = self.__file_object.get_random_word(category) # Juhuslik sõna
        #print(self.__new_word) #andis konsooli suvalise sõna
        self.__user_word = [] # Algseis
        self.__counter = 0 # Algseis
        self.__all_user_chars = [] # Algseis

        # Asenda sõnas kõik tähed allkriipsuga M A J A => _ _ _ _
        for x in range(len(self.__new_word)):
            self.__user_word.append('_')
        #print(self.__new_word, self.__user_word) # konsooli: kasvuhoone ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_']


    def get_user_input(self, user_input):
        #User_input on sisestuskasti kirjutatud tähed
        if user_input:
            user_char = user_input[:1] #Esimene märk sisestuses
            if user_char.lower() in self.__new_word.lower():
                self.change_user_input(user_char) # Leiti täht
            else: #Seda tähte pole sõnas
                self.__counter += 1
                self.__all_user_chars.append(user_char.upper())
        else: #Kasutaja ei sisestanud midagi
            self.__counter += 1



    def change_user_input(self, user_char):
        # Asenda kõik _ leitud tähega
        current_word = self.char_to_list(self.__new_word) #Listi kujul äraarvatav sõna
        x = 0
        for c in current_word: # c on üks täht listist
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
        return ', '.join(self.__all_user_chars) #List tehakse komaga eraldatud stringiks

    def save_player_score(self, name, seconds):
        today = datetime.now().strftime('%Y-%m-%d %T') #Hetke kuupäev ja kell 2025-02-06 14:12:29
        if not name.strip(): #Kui nime ei ole
            name = random.choice(['Teadmata', 'Tundmatu', 'Unknown'])
        with open(self.__scoreboard.file_path, 'a', encoding='utf-8') as file:
            line = ';'.join([name.strip(), self.__new_word, self.get_all_user_chars(), str(seconds), today])
            file.write(line + '\n')


    #GETTERS
    @property
    def image_files(self):
        """Tagastab piltide listi"""
        return self.__image_files

    @property
    def categories(self):
        """Tagastab kategooriate listi"""
        return self.__categories

    @property
    def user_word(self):
        """Tagastab kasutaja leitud tähed"""
        return self.__user_word

    @property
    def counter(self):
        return self.__counter




