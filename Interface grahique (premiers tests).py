import hashlib
from tkinter import *
from tkinter import filedialog
from tkinter import Radiobutton
from tkinter import tix

# Fonction de hashage avec option d'ajout de sel
def hashMsg():
    sel = selectedSalt.get()

    m = hashlib.new(varGr.get())
    if (sel != "" and sel != "Pas de sel"):
        m.update(sel.encode())
    m.update(textAHasher.get().encode())
    hashAnswer.set("Hash : "+m.hexdigest().upper())


# créer une première fenêtre
window = tix.Tk()

# personnaliser cette fenêtre
window.title("NotACrypter")
window.geometry("1370x720")
window.minsize(800, 450)
window.config(background='#555555')

# Fonction ouvrant la fenêtre permettant d'ajouter un sel en BDD
def createSalt():
    newSalt = Tk()

    newSalt.title("Ajout d'un sel")
    newSalt.geometry("385x100")
    newSalt.minsize(385, 100)
    newSalt.config(background='#555555')

    label_name = Label(newSalt, text="Nom", font=(
        "Courrier", 14), bg='#555555', fg='white').place(x=3, y=0)

    entry_name = Entry(newSalt, width=50)
    entry_name.pack()
    entry_name.place(x=78, y=5)

    label_saltValue = Label(newSalt, text="Valeur", font=(
        "Courrier", 14), bg='#555555', fg='white').place(x=3, y=30)

    entry_saltvalue = Entry(newSalt, width=50)
    entry_saltvalue.pack()
    entry_saltvalue.place(x=78, y=34)

    button_addSalt = Button(
        newSalt, text='Ajouter le sel', width=53).place(x=3, y=70)

# Fonction ouvrant la fenêtre listant tous les sels
def openSalt():

    saltPanel = Tk()

    saltPanel.title("Sels")
    saltPanel.geometry("500x160")
    saltPanel.minsize(500, 160)
    saltPanel.config(background='#555555')

    allSalt = Listbox(saltPanel)
    for i in range(20):
        allSalt.insert(i, str(i))
    allSalt.pack()
    allSalt.place(x=0, y=0)

    addSalt = Button(saltPanel, text='Ajouter', width=10,
                     command=createSalt).place(x=125, y=0)

    editSalt = Button(saltPanel, text='Editer', width=10).place(x=125, y=25)

    deleteSalt = Button(saltPanel, text='Supprimer',
                        width=10).place(x=125, y=50)

    saltPanel.mainloop()

# Fonction ouvrant la fenêtre permettant d'ajouter une clé AES en BDD
def createAES():
    newAES = Tk()

    newAES.title("Ajout d'une clé AES")
    newAES.geometry("385x100")
    newAES.minsize(385, 100)
    newAES.config(background='#555555')

    label_name = Label(newAES, text="Nom", font=(
        "Courrier", 14), bg='#555555', fg='white').place(x=3, y=0)

    entry_AESname = Entry(newAES, width=50)
    entry_AESname.pack()
    entry_AESname.place(x=78, y=5)

    label_AESValue = Label(newAES, text="Valeur", font=(
        "Courrier", 14), bg='#555555', fg='white').place(x=3, y=30)

    entry_AESvalue = Entry(newAES, width=50)
    entry_AESvalue.pack()
    entry_AESvalue.place(x=78, y=34)

    button_addAES = Button(
        newAES, text='Ajouter le sel', width=53).place(x=3, y=70)

# Fonction ouvrant la fenêtre listant toutes les clés AES
def openAES():

    aesPanel = Tk()

    aesPanel.title("Clés AES")
    aesPanel.geometry("500x160")
    aesPanel.minsize(500, 160)
    aesPanel.config(background='#555555')

    allAES = Listbox(aesPanel)
    for i in range(20):
        allAES.insert(i, str(i))
    allAES.pack()
    allAES.place(x=0, y=0)

    addAES = Button(aesPanel, text='Ajouter', width=10,
                    command=createAES).place(x=125, y=0)

    editAES = Button(aesPanel, text='Editer', width=10).place(x=125, y=25)

    deleteAES = Button(aesPanel, text='Supprimer',
                       width=10).place(x=125, y=50)

    aesPanel.mainloop()


# Titres
label_title = Label(window, text="Fonction de hashage", font=(
    "Courrier", 14), bg='#555555', fg='white', height='10').place(x=70, y=40)

label_title4 = Label(window, text="Votre sel", font=(
    "Courrier", 14), bg='#555555', fg='white', height='1').place(x=110, y=250)

label_title2 = Label(window, text="Votre document", font=(
    "Courrier", 14), bg='#555555', fg='white', height='10').place(x=110, y=275)

label_title3 = Label(window, text="Votre message", font=(
    "Courrier", 14), bg='#555555', fg='white', height='1').place(x=110, y=300)

label_title5 = Label(window, text="Clés AES", font=(
    "Courrier", 14), bg='#555555', fg='white', height='1').place(x=110, y=200)

selectedSalt = StringVar()

# Liste des sels disponibles
availableSalt = tix.ComboBox(
    window, dropdown=1, variable=selectedSalt)
availableSalt.insert(0, "Pas de sel")
availableSalt.insert(1, "Valentin")
availableSalt.insert(2, "Lucas")
availableSalt.pack()
availableSalt.place(x=220, y=250)

# Listes des clés AES disponibles
availableAES = tix.ComboBox(
    window, dropdown=1, variable=selectedSalt)
availableAES.insert(0, "Pas de clé AES")
availableAES.insert(1, "Alexandre")
availableAES.insert(2, "Lucas")
availableAES.pack()
availableAES.place(x=220, y=200)

hashAnswer = StringVar()

# Affichage du résultats du hash
hashResult = Label(window, textvariable=hashAnswer, font=(
    "Courrier", 14), bg='#555555', fg='white', height='1')
hashResult.pack()
hashResult.place(x=125, y=560)

# Fonction d'ouverture de fichier
def mfileopen():
    file1 = filedialog.askopenfile()
    label_file = Label(window, text=file1, font=(
        "Courrier", 10), bg='#555555', fg='white', height='10').place(x=550, y=310)


varGr = StringVar()

# Tous les boutons
button = Button(window, text="Sélectionner un document", width=30,
                command=mfileopen).place(x=300, y=377)

openSalt = Button(window, text="Gérer les sels", width=30,
                  command=openSalt).place(x=1100, y=600)

openAES = Button(window, text="Gérer les clés AES", width=30,
                 command=openAES).place(x=1100, y=630)

EncryptButton = Button(window, text="Chiffrer", width=20,
                 command=openAES).place(x=125, y=630)

DecipherButton = Button(window, text="Déchiffrer", width=20,
                 command=openAES).place(x=325, y=630)

# Champsà remplir pour hasher un message
textAHasher = Entry(window, width=50)
textAHasher.pack()
textAHasher.place(x=300, y=305)

hashing_button = Button(text="Hasher", width=50,
                        command=hashMsg).place(x=125, y=525)

# Radio buttons permettant de choisir notre algorithme de hashage
vals = ['sha1', 'sha256', 'sha512', 'md5', 'blake2b']
etiqs = ['SHA-1', 'SHA-256', 'SHA-512', 'MD5', 'Blake2B']
varGr.set(vals[0])
for i in range(5):
    b = Radiobutton(window, variable=varGr,
                    text=etiqs[i], value=vals[i], activebackground="#555555", bg='#555555', activeforeground="white", foreground="white", selectcolor="black")
    b.pack(side='left', expand=1)
    b.place(x=(100*i)+300, y=140)

# Afficher la fenêtre
window.mainloop()
