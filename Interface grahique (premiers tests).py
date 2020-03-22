from tkinter import *

#créer une première fenêtre
window = Tk()

#personnamiser cette fenêtre
window.title("NotACrypter")
window.geometry("1080x720")
window.minsize(800, 450)
window.config(background='#555555')

#premier texte
label_title = Label (window, text="Fonction de hashage", font=("Courrier", 18), bg='#555555', fg='white', height='10')
label_title.grid(column=0)

optionlist = [
    "SHA-1",
    "SHA-256",
    "SHA-512",
    "MD5",
    "Blake2"
]

variable = tk.StingVar(window)
varible.set(OptionList[0])

opt = tk.OptionMenu(app, variable, *OptionList)
opt.config(width=90, font=('Helvetica', 12))
opt.pack()

#afficher
window.mainloop()
