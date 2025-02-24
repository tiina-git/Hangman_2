import time


class Stopwatch:
    def __init__(self, lbl_time): #Tuleb Viewst anda kaasa aja label
        self.__lbl_time = lbl_time
        self.__seconds = 0 #Aeg sekundites
        self.__running = False

    def start(self):
        self.__running = True
        self.update()

    def update(self):
        if self.__running:
            if self.__seconds == 0:
                display = '00:00:00'
            else:
                display = time.strftime('%H:%M:%S', time.gmtime(self.__seconds))

            self.__lbl_time['text'] = display #Muuda aeg labelil
            self.__lbl_time.after(1000, self.update) # oota sekund ja kutsu ennast uuesti välja
            self.__seconds += 1 #Suurenda sekundeid ühe võrra

    def stop(self):
        """Peata stopper"""
        self.__running = False

    def reset(self):
        self.__seconds = 0
        self.__lbl_time['text'] = '00:00:00'


    @property
    def seconds(self): #GETTER
        """Tagasta mänguaja sekundid"""
        return self.__seconds



