import hashlib
from tkinter import *
from tkinter import filedialog
from tkinter import Radiobutton
from tkinter import tix


def hashMsg():
    algo = varGr.get()
    sel = selectedSalt.get()
    print(algo)
    if algo == 'sha1':
        m = hashlib.sha1()
    elif algo == 'sha256':
        m = hashlib.sha256()
    elif algo == 'sha512':
        m = hashlib.sha512()
    elif algo == 'md5':
        m = hashlib.md5()
    elif algo == 'blake2b':
        m = hashlib.blake2b()
    else:
        print('L\'algorithme n\'est pas connu par NotACrypter')
        return 0
    if (sel != "" or sel != "Pas de sel"):
        m.update(sel.encode())
    m.update(textAHasher.get().encode())
    hashAnswer.set("Hash : "+m.hexdigest())


# créer une première fenêtre
window = tix.Tk()


def openSalt():

    saltPanel = Tk()

    saltPanel.title("Sels")
    saltPanel.geometry("500x150")
    saltPanel.minsize(500, 150)
    saltPanel.config(background='#555555')

    saltPanel.mainloop()


def openAES():

    aesPanel = Tk()

    aesPanel.title("AES")
    aesPanel.geometry("500x150")
    aesPanel.minsize(500, 150)
    aesPanel.config(background='#555555')

    aesPanel.mainloop()


# personnaliser cette fenêtre
window.title("NotACrypter")
window.geometry("1370x720")
window.minsize(800, 450)
window.config(background='#555555')

# premier texte
label_title = Label(window, text="Fonction de hashage", font=(
    "Courrier", 14), bg='#555555', fg='white', height='10').place(x=70, y=75)

label_title2 = Label(window, text="Votre document", font=(
    "Courrier", 14), bg='#555555', fg='white', height='10').place(x=110, y=275)

label_title3 = Label(window, text="Votre message", font=(
    "Courrier", 14), bg='#555555', fg='white', height='1').place(x=110, y=275)

label_title4 = Label(window, text="Votre sel", font=(
    "Courrier", 14), bg='#555555', fg='white', height='1').place(x=110, y=240)

selectedSalt = StringVar()

availableSalt = tix.ComboBox(
    window, dropdown=1, variable=selectedSalt)
availableSalt.insert(0, "Pas de sel")
availableSalt.insert(1, "Valentin")
availableSalt.insert(2, "Lucas")
availableSalt.pack()
availableSalt.place(x=220, y=240)

hashAnswer = StringVar()

hashResult = Label(window, textvariable=hashAnswer, font=(
    "Courrier", 14), bg='#555555', fg='white', height='1')
hashResult.pack()
hashResult.place(x=125, y=560)


def mfileopen():
    file1 = filedialog.askopenfile()
    label_file = Label(window, text=file1, font=(
        "Courrier", 10), bg='#555555', fg='white', height='10').place(x=550, y=310)


varGr = StringVar()

button = Button(window, text="Sélectionner un document", width=30,
                command=mfileopen).place(x=300, y=377)

openSalt = Button(window, text="Gérer les sels", width=30,
                  command=openSalt).place(x=1100, y=600)

openAES = Button(window, text="Gérer les clés AES", width=30,
                 command=openAES).place(x=1100, y=630)

textAHasher = Entry(window, width=50)
textAHasher.pack()
textAHasher.place(x=300, y=280)

hashing_button = Button(text="Hasher", width=50,
                        command=hashMsg).place(x=125, y=525)

vals = ['sha1', 'sha256', 'sha512', 'md5', 'blake2b']
etiqs = ['SHA-1', 'SHA-256', 'SHA-512', 'MD5', 'Blake2B']
varGr.set(vals[0])
for i in range(5):
    b = Radiobutton(window, variable=varGr,
                    text=etiqs[i], value=vals[i], activebackground="#555555", bg='#555555', activeforeground="white", foreground="white", selectcolor="black")
    b.pack(side='left', expand=1)
    b.place(x=(100*i)+300, y=175)

# afficher
window.mainloop()
