import random
from tkinter import simpledialog, messagebox
from tkinter.constants import NORMAL, DISABLED



from models.Database import Database
from models.Leaderboard import Leaderboard
from models.Stopwatch import Stopwatch
from models.Timer import Timer


class Controller:
    def __init__(self, model, view):
        self.database = Database()
        self.model = model
        self.view = view
        self.stopwatch = Stopwatch(self.view.lbl_time)

        # Ajasti loomine (tiitelriba aja jaoks)
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
        self.view.btn_new['state'] = DISABLED # Uut mängu alustada ei saa, kui käib
        self.view.btn_send['state'] = NORMAL
        self.view.btn_cancel['state'] = NORMAL
        self.view.char_input['state'] = NORMAL
        self.view.char_input.focus()
        self.view.cmb_category['state'] = DISABLED

    def buttons_for_not_game(self):
        self.view.btn_new['state'] = NORMAL
        self.view.btn_send['state'] = DISABLED
        self.view.btn_cancel['state'] = DISABLED
        self.view.char_input.delete(0,'end')  # Tühjenda sisestuskast
        self.view.char_input['state'] = DISABLED
        self.view.cmb_category['state'] = NORMAL

    def btn_new_callback(self):
        self.view.set_btn_new_callback(self.btn_new_click) # meetod sulgudeta

    def btn_cancel_callback(self):
        self.view.set_btn_cancel_callback(self.btn_cancel_click)

    def btn_new_click(self):
        self.buttons_for_game() # Nupu majandus

        # Seadisdtab juhusliku sõna kategooria järgi, asendab tähed kriipsudega
        selected_category = self.view.cmb_category.get()
        #self.model.start_new_game(self.view.cmb_category.current(), self.view.cmb_category.get()) # id, kategooria ja index
        self.model.start_new_game(selected_category)
        # Näita kasutajale 'sõna'
        self.view.lbl_result.config(text=self.model.user_word)

        # Vigaste tähtede resettimine
        self.view.lbl_error.config(text='Vigased tähed', fg = 'black')
        self.view.change_image(0)

        # Muuda pilti
        self.view.change_image(self.model.counter)
        self.timer.start() # käivita timer 5 sekundiks
        self.stopwatch.reset() # Eelmise mängu nullimine
        self.stopwatch.start()  # Käivita aeg

    def btn_scoreboard_callback(self):
        self.view.set_btn_scoreboard_callback(self.btn_scoreboard_click)

    def btn_send_callback(self):
        self.view.set_btn_send_callback(self.btn_send_click)

    def btn_cancel_click(self):
        self.buttons_for_not_game()
        self.stopwatch.stop()
        self.timer.stop()
        self.view.lbl_result.config(text=self.model.user_word)
        self.view.title(self.model.titles[0])  # Esimene listi element title listist

    def btn_send_click(self):
        self.model.get_user_input(self.view.char_input.get().strip()) # Saada sisestus
        self.view.lbl_result.config(text=self.model.user_word)   # Uuenda tulemus
        self.view.lbl_error.config(text=f'Vigased tähed: {self.model.get_all_user_chars()}')
        self.view.char_input.delete(0, 'end')
        if self.model.counter >0 : # counter on pildi indeks
            self.view.lbl_error.config(fg = 'red')
            self.view.change_image(self.model.counter) # Muuda pilti - muutuja
            self.is_game_over()


    def btn_scoreboard_click(self):             # Edetabeli nupp
        #lb = Leaderboard()
        #data = lb.read_leaderboard()
        db = Database()
        lb_data = self.database.get_leaderboard()

        if lb_data:
            print(f"Edetabel pole enam tühi...")     # Test kas andmed on olemas
            popup_window = self.view.create_popup_window()
            self.view.generate_scoreboard(popup_window, lb_data)
        else:
            messagebox.showinfo('Teade', 'Edetabelisse pole mängijaid lisatud.')


    def is_game_over(self):
        # Mängu lõpp, pildid otsas või kriipsud otsas
        if self.model.counter >= 11 or '_' not in self.model.user_word:
            self.stopwatch.stop()
            self.timer.stop()
            self.buttons_for_not_game()  # Nupud aktiivseks
            player_name = simpledialog.askstring('Mäng on läbi', 'Kuidas on mängija nimi ?', parent=self.view)
            # print(player_name)

            # self.model.save_player_score(player_name, self.stopwatch.seconds)
            self.model.save_player_score(player_name, self.stopwatch.seconds)
            messagebox.showinfo('Teade', 'Oled lisatud edetabelisse.')
            self.view.title(self.model.titles[0])  # Esimene listi element title listist


    def change_title(self):
        #new_title = self.model.get_random_title()
        new_title = random.choice(self.model.titles)
        self.view.title(new_title)

    def reset_timer(self):
        self.timer.start()


