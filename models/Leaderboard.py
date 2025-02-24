import os

from models.Score import Score


class Leaderboard:
    def __init__(self):
        self.__file_path = os.path.join('databases', 'leaderboard.txt')
        self.check_file() # Kontrolli faili olemasolu ja kui pole, siis tee


    def check_file(self):
        if not os.path.exists(self.__file_path):
            self.create_leaderboard()

    def create_leaderboard(self):
        header = ['name', 'word', 'letters', 'game length', 'game time']
        with open(self.__file_path, 'a', encoding='utf-8') as f: # 'a' on append ehk lisa
            f.write(';'.join(header) + '\n')

    def read_leaderboard(self):
        leaderboard = []
        with open(self.__file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines() # Kõik read listi

            if not lines: #Ridu ei ole failis
                return [] # Tühi list

            for line in lines[1:]: # hakka lugema alates teisest reast
                line = line.strip() # Korrastame rea
                name, word, letters, game_length, game_time = line.split(';')
                leaderboard.append(Score(name, word, letters, int(game_length), game_time))

            leaderboard = sorted(leaderboard, key=lambda x: (x.game_length, len(x.letters.split(', ')))) # Sorteerida kestvuse järgi

        return leaderboard



    @property
    def file_path(self):
        return self.__file_path # Failinimi koos kaustaga database/leaderboard.txt