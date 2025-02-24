import random
from tkinter import simpledialog, messagebox
from tkinter.constants import DISABLED, NORMAL

from models.Leaderboard import Leaderboard
from models.Stopwatch import Stopwatch
from models.Timer import Timer


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.stopwatch = Stopwatch(self.view.lbl_time)

        #ajasti loomine
        self.timer = Timer(
            scheduled_callback=self.view.after,
            cancel_callback=self.view.after_cancel,
            interval=5000, #5sekundit
            callback=self.change_title,
        )


        # Nuppude callback seaded
        self.btn_new_callback()
        self.btn_cancel_callback()
        self.btn_send_callback()
        self.btn_scoreboard_callback()
        self.view.set_timer_reset_callback(self.reset_timer) #Ajasti värk

        #Enter klahvi funktsionaalsus
        self.view.bind('<Return>', lambda e: self.btn_send_click()) #Return tähistas enter klahvi

    def buttons_for_game(self):
        self.view.btn_new['state'] = DISABLED #Kui mäng on alanud, siis uue mängu nuppu kohe vajutada ei saa
        self.view.btn_send['state'] = NORMAL
        self.view.btn_cancel['state'] = NORMAL
        self.view.char_input['state'] = NORMAL
        self.view.char_input.focus()
        self.view.cmb_category['state'] = DISABLED

    def buttons_for_not_game(self):
        self.view.btn_new['state'] = NORMAL
        self.view.btn_send['state'] = DISABLED
        self.view.btn_cancel['state'] = DISABLED
        self.view.char_input.delete(0, 'end') #Tühjenda sisestuskasti sisu (0, 'end') tähendab algusest lõpuni
        self.view.char_input['state'] = DISABLED
        self.view.cmb_category['state'] = NORMAL

    def btn_new_callback(self):
        self.view.set_btn_new_callback(self.btn_new_click) #meetod iilma sulgudeta

    def btn_cancel_callback(self):
        self.view.set_btn_cancel_callback(self.btn_cancel_click) # Teeb cancel nupu toimivaks

    def btn_send_callback(self):
        self.view.set_btn_send_callback(self.btn_send_click) # Teeb Saada nupu toimivaks

    def btn_scoreboard_callback(self):
        self.view.set_btn_scoreboard_callback(self.btn_scoreboard_click) #teeb nupu Edetabel toimivaks


    def btn_new_click(self):
        self.buttons_for_game() # Nupu majandus
        """Seadista juhuslik sõna kategooria järgi ja asendab tähed _ -ga"""
        self.model.start_new_game(self.view.cmb_category.current(), self.view.cmb_category.get()) # Current annab indeksiga ja get annab sõnaga
        #Näita "sõna" kasutajale. Sõna on allkriipsudega
        self.view.lbl_result.config(text=self.model.user_word)
        #Vigaste tähtede resettimine
        self.view.lbl_error.config(text='Vigased tähed', fg='black') #fg = näovärv
        #Muuda pilti
        self.view.change_image(0) # Algab piltide lugemine nullist
        self.timer.start() #Käivita title juslikkus (5 sek)
        self.stopwatch.reset()
        self.stopwatch.start()


        self.stopwatch.reset() # Eelmine mäng nullitakse ära
        self.stopwatch.start() #Käivita aeg


    def btn_cancel_click(self):
        self.buttons_for_not_game()
        self.stopwatch.stop() # Peatab stopperi
        self.timer.stop() #Peata title jushuslikkus
        self.view.lbl_result.config(text=self.model.user_word)
        self.view.title(self.model.titles[0])  # Esimene element listist


    def btn_send_click(self):
        #print('Saada') # Kuvab kosooli "Saada"
        self.model.get_user_input(self.view.char_input.get().strip()) #Saada sisestus
        self.view.lbl_result.config(text=self.model.user_word) # Uuenda tulemust
        self.view.lbl_error.config(text=f'Vigased tähed: {self.model.get_all_user_chars()}')
        #Sisestuskast tühjaks
        self.view.char_input.delete(0, 'end')
        if self.model.counter > 0:
            self.view.lbl_error.config(fg='red') #Muudab vigase teksti punaseks
            self.view.change_image(self.model.counter) # Muudab pilti

        self.is_game_over()


    def btn_scoreboard_click(self):
        lb = Leaderboard()
        data = lb.read_leaderboard()
        popup_window = self.view.create_popup_window()
        self.view.generate_scoreboard(popup_window, data)

    def is_game_over(self):
        if self.model.counter >= 11 or '_' not in self.model.user_word:
            self.stopwatch.stop() # Aeg jääb seisma
            self.timer.stop() #Peata title jaoks
            self.buttons_for_not_game() # Nupu majandus
            player_name = simpledialog.askstring('Mäng on läbi!', 'Kuidas on mängija nimi?', parent=self.view) #parent on see, et millise akna peale läheb
            messagebox.showinfo('Teade', 'Oled lisatud edetabelisse!')
            self.model.save_player_score(player_name, self.stopwatch.seconds)
            self.view.title(self.model.titles[0]) #Esimene element listist


    def change_title(self):
        new_title = random.choice(self.model.titles)
        self.view.title(new_title)


    def reset_timer(self):
        self.timer.start()






