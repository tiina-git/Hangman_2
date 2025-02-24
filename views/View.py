import os
import time
from datetime import datetime
from tkinter import * #* impordib kõik
from tkinter import font, messagebox, ttk
from tkinter.ttk import Combobox, Treeview

from PIL import ImageTk, Image

from models.FileObject import FileObject


class View(Tk):
    def __init__(self, model):
        super().__init__() # See on Tk jaoks
        self.model = model #app.py failis loodud mudel

        #Põhiakna omadused
        self.__width = 585 # Privaatne muutuja akna laius #__ tähendab et seda väärtust ei saa väljaspool seda mudelit muuta.
        self.__height = 200 #Privaatne muutuja akna kõrgus
        self.title("Poomismäng 2025") #Kasutajaliides on eesti keeles. # Tiitelriba tekst
        self.center(self, self.__width, self.__height) #Paigutab põhiakna ekraani kesekele.

        #Kirjastiilid
        self.__big_font = font.Font(family='Courier', size=20, weight='bold') #Kollane taust
        self.__default = font.Font(family='Verdana', size=12) # Vaikimisi kirjastiil (lbl,btn)
        self.__default_bold = font.Font(family='Verdana', size=12, weight='bold')

        # Kogustiil vormi stiil
        self.option_add('*Font', self.__default)

        # Loo kolm paneeli (Frame)
        self.__frame_top, self.__frame_bottom, self.__frame_image = self.create_frames()

        # Loome neli nuppu
        self.__btn_new, self.__btn_scoreboard, self.__btn_cancel, self.__btn_send = self.create_buttons()

        # Loome pildi "koha"
        self.__image = ImageTk.PhotoImage(Image.open('images/hang11.png'))
        self.__lbl_image = None

        # Loome "kolm" labelit
        self.__lbl_error, self.__lbl_time, self.__lbl_result = self.create_labels()

        # Loome rippmenüü
        self.__cmb_catecory = self.create_combobox()

        #Loome sisestuskasti
        self.__char_input = self.create_entry()

        # Sidumine hiire ja klaviatuuri tegevustega
        self.bind('<Motion>', self.reset_timer)
        self.bind('<Key>', self.reset_timer)
        self.timer_reset_callback = None



    @staticmethod
    def center(win, width, height):
        x = int((win.winfo_screenwidth() / 2) - (width / 2))
        y = int((win.winfo_screenheight() / 2) - (height / 2))
        win.geometry(f'{width}x{height}+{x}+{y}') #Sellega tuleb mängu aken ekraani keskele.

    def create_frames(self):
        top = Frame(self, height=50, background='lightblue')
        bottom = Frame(self, background='lightyellow')
        image = Frame(top, background='lightsalmon', width=130, height=130)

        # Paiguta paneelid põhiaknale
        top.pack(fill=BOTH)
        bottom.pack(fill=BOTH, expand=True)
        image.grid(row=0, column=3, padx=5, pady=5, rowspan=4) # Rowspan tähendab üle 4 rea

        return top, bottom, image # Tagastab vidina

    def create_buttons(self):
        new = Button(self.__frame_top, text='Uus mäng')
        scoreboard = Button(self.__frame_top, text='Edetabel')
        cancel = Button(self.__frame_top, text='Katkesta', state=DISABLED) #disabled ei lase suvalisel hetkel seda vajutada
        send = Button(self.__frame_top, text='Saada', state=DISABLED)

        new.grid(row=0, column=0, padx=5, pady=2, sticky=EW) #Sticky - veerg venitatakse kasti laiuseks
        scoreboard.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        cancel.grid(row=0, column=2, padx=5, pady=2, sticky=EW)
        send.grid(row=2, column=2, padx=5, pady=2, sticky=EW)

        return new, scoreboard, cancel, send

    def create_labels(self):
        Label(self.__frame_top, text='Kategooria').grid(row=1, column=0, padx=5, pady=2, sticky=EW) #Labeli omadusi ei saa muuta (värv, stiil jms)
        Label(self.__frame_top, text='Sisesta täht').grid(row=2, column=0, padx=5, pady=2, sticky=EW) # Loome labeli ja paneme kohe paika (pole vaja hiljem muuta)

        #Error, Time, Result
        error = Label(self.__frame_top, text='Vigased tähed', anchor=W, font=self.__default_bold) # W tähendab et joondatakse lahtri vasakusse serva
        time = Label(self.__frame_top, text='00:00:00')
        result = Label(self.__frame_bottom, text='m _ _ _ _ m _'.upper(), font=self.__big_font, background='lightyellow')

        error.grid(row=3, column=0, padx=5, pady=2, sticky=EW, columnspan=3)
        time.grid(row=1, column=2, padx=5, pady=2, sticky=EW)
        result.pack(pady=10)

        #Pildi paigutamine
        self.__lbl_image = Label(self.__frame_image, image=str(self.__image))
        self.__lbl_image.pack()

        return error, time, result

    def create_combobox(self):
        combo = Combobox(self.__frame_top)
        combo['values'] = self.model.categories #Selleks pidin tegema Modelis @propertise
        combo.current(0) #Paneb vaikimisi sinna selle Vali kategooria
        combo.grid(row=1, column=1, padx=5, pady=2, sticky=EW)

        return combo

    def create_entry(self):
        char = Entry(self.__frame_top, justify='center')
        char['state'] = 'disabled'
        char.focus()
        char.grid(row=2, column=1, padx=5, pady=2, sticky=EW)

        return char

    @staticmethod
    def show_message(message):
        root = Tk()
        root.withdraw()  # Peidab loodava akna
        messagebox.showerror("Viga", f'{message}')
        #root.destroy()


    """Pildi muutmine vastavalt image pildi numbrile - id"""
    def change_image(self, image_id):
        self.__image = ImageTk.PhotoImage(Image.open(self.model.image_files[image_id]))
        self.__lbl_image.configure(image=self.__image)
        self.__lbl_image.image = str(image_id)

    def set_btn_new_callback(self, callback):
        self.__btn_new.config(command=callback)

    def set_btn_cancel_callback(self, callback):
        self.__btn_cancel.config(command=callback)

    def set_btn_send_callback(self, callback):
        self.__btn_send.config(command=callback)


    def set_btn_scoreboard_callback(self, callback):
        self.__btn_scoreboard.config(command=callback) #Edetabeli välja kutsumine nupust Edetabel

    def set_timer_reset_callback(self, callback):
        self.timer_reset_callback = callback

    def reset_timer(self, event=None):
        if self.timer_reset_callback:
            self.timer_reset_callback()

    def create_popup_window(self):
        """Loome akna, kus kuvatakse edetabel"""
        style = ttk.Style()
        style.configure('Treeview', font=self.__default)
        style.configure('Treeview.Heading', font=self.__default_bold)

        top = Toplevel(self) #Anname põhiakna kaasa
        top.title('Edetabel')
        top_w = 750
        top_h = 300
        top.resizable(False, False)
        top.grab_set() #Aken on põhiakna peal (ei saa põhiakend sulgeda, enne kui pealmine pole kinni pandud)
        top.focus()

        frame = Frame(top)
        frame.pack(fill=BOTH, expand=True)
        self.center(top, top_w, top_h) #Paiguta aken ekraani kesekele

        return frame

    def generate_scoreboard(self, frame, data):
        if len(data) > 0:
            # Table View
            self.my_table = Treeview(frame)

            # Vertikaalne kerimisriba
            vsb = Scrollbar(frame, orient=VERTICAL, command=self.my_table.yview)
            vsb.pack(side=RIGHT, fill=Y)
            self.my_table.configure(yscrollcommand=vsb.set)

            # Veeru ID-d
            self.my_table['columns'] = ('name', 'word', 'letters', 'game_length', 'date_time')

            # Veergude seaded
            self.my_table.column('#0', width=0, stretch=NO)
            self.my_table.column('name', anchor=W, width=100)
            self.my_table.column('word', anchor=W, width=100)
            self.my_table.column('letters', anchor=CENTER, width=100)
            self.my_table.column('game_length', anchor=CENTER, width=75)
            self.my_table.column('date_time', anchor=CENTER, width=100)

            #Veergude pealkirjad
            self.my_table.heading('#0', text='', anchor=CENTER)
            self.my_table.heading('name', text='Nimi', anchor=CENTER)
            self.my_table.heading('word', text='Sõna', anchor=CENTER)
            self.my_table.heading('letters', text='Valed tähed', anchor=CENTER)
            self.my_table.heading('game_length', text='Kestvus', anchor=CENTER)
            self.my_table.heading('date_time', text='Mängu aeg', anchor=CENTER)

            # Topelt klikk real
            self.my_table.bind('<Double-1>', self.on_row_double_click)




            #Lisa andmed tabelisse
            x = 0
            for score in data:
                dt = datetime.strptime(score.game_time, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %T') # Teeme kuupäeva ja kella korda
                sec = time.strftime('%H:%M:%S', time.gmtime(int(score.game_length)))

                self.my_table.insert(parent='', index='end', iid=str(x), text='', values=(score.name, score.word, score.letters, sec, dt))
                x += 1

            self.my_table.pack(fill=BOTH, expand=True)

    def on_row_double_click(self, event):
        # Võta valitud rida
        selected_item = self.my_table.selection()
        if selected_item:
            row_values = self.my_table.item(selected_item, 'values')
            #Näitab popup akent infoga
            messagebox.showinfo("Informatsioon", message=f'Nimi: {row_values[0]}\nSõna: {row_values[1]}\nVigased tähed: {row_values[2]}\nMängu pikkus: {row_values[3]}\nMängu aeg: {row_values[4]}\n', parent=self.my_table)


    #GETTERS

    @property
    def btn_new(self):
        return self.__btn_new

    @property
    def btn_scoreboard(self):
        return self.__btn_scoreboard

    @property
    def btn_cancel(self):
        return self.__btn_cancel

    @property
    def btn_send(self):
        return self.__btn_send

    @property
    def char_input(self):
        return self.__char_input

    @property
    def cmb_category(self):
        return self.__cmb_catecory

    @property
    def lbl_time(self):
        return self.__lbl_time

    @property
    def lbl_error(self):
        return self.__lbl_error

    @property
    def lbl_result(self):
        return self.__lbl_result
