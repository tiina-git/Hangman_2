import sys
from tkinter import Tk, messagebox

from controllers.Controller import Controller
from models.Model import Model
from views.View import View


if __name__ == '__main__':
    try:
        model = Model() #Loo mudel #See mudel jookseb koguaeg kaasas.
        view = View(model) # Loo view andes kaasa mudel
        Controller(model, view)
        view.mainloop() # Viimane rida koodis
    except FileNotFoundError as error:
        #print(f'Viga: {error}')
        View.show_message(error)
        sys.exit(1) #Veaga lõpetamine on 1
    except ValueError as error:
        View.show_message(error)
        sys.exit(1)
    except Exception as error:
        #print(f'Tekkis ootamatu viga: {error}')
        View.show_message(error)
        sys.exit(1) # Kood lõpetab töö