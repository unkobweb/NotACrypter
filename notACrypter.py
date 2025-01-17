import hashlib
from tkinter import *
from tkinter import filedialog
from tkinter import Radiobutton
from tkinter import tix
import sqlite3
from sqlite3 import Error
from cryptography.fernet import Fernet
import subprocess

# Chemin vers le fichier .db pour sqlite3
database = r"./pythonsqlite.db"

# Création des deux tables si elles n'existent pas
sql_create_salt_table = """ CREATE TABLE IF NOT EXISTS salt (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    salt text NOT NULL
                                ); """

sql_create_aes_table = """CREATE TABLE IF NOT EXISTS aes (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                key text NOT NULL
                            );"""

# Fonction connection à la base de donnée


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

# Fonction de création d'une table


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


conn = create_connection(database)

# Création des tables
if conn is not None:
    create_table(conn, sql_create_salt_table)

    create_table(conn, sql_create_aes_table)
else:
    print("Error! cannot create the database connection.")

# Fonction qui permet le hash d'un message ou d'un fichier


def hashMsg():
    # On récupère l'algorythme de hashage
    m = hashlib.new(varGr.get())
    sel = ""

    # Si l'utilisateur à choisi un sel on va le récupérer et l'incorporer au début du hash
    if (selectedSalt.get() != "" and selectedSalt.get() != "Pas de sel"):
        cur = conn.cursor()
        cur.execute("SELECT * FROM salt WHERE name = ?",
                    [selectedSalt.get()])

        rows = cur.fetchall()

        sel = rows[0][2]

    if (textAHasher.get() != ""):   # Si l'utilisateur veut hasher un message
        if (sel != ""):
            m.update(sel.encode())
        m.update(textAHasher.get().encode())
        hashAnswer.set(m.hexdigest().upper())
    elif (selectedFile.get() != ""):  # Si l'utilisateur veut hasher un fichier
        # Ouverture du fichier en mode 'rb' pour récupérer les bytes qui composent ce fichier
        with open(selectedFile.get(), 'rb') as afile:
            buf = afile.read()
            if (sel != ""):
                m.update(sel.encode())
            m.update(buf)
            hashAnswer.set(m.hexdigest().upper())

# Fonction qui permet le chiffrement de message / fichier


def encrypt():
    if (selectedAES.get() != ''):   # On vérifie que l'utilisateur a bien choisi une clé AES
        # On récupère la clé AES
        cur = conn.cursor()
        cur.execute("SELECT * FROM aes WHERE name = ?",
                    [selectedAES.get()])

        rows = cur.fetchall()

        aes = rows[0][2]

        f = Fernet(aes.encode())
        if (textAHasher.get() != ""):  # Si l'utilisateur veut chiffrer un message
            m = hashlib.md5()
            m.update(textAHasher.get().encode())
            nameOfFile = m.hexdigest()
            with open('./output/encrypted/'+nameOfFile+'.txt.aes', 'w') as newFile:
                newFile.write(f.encrypt(textAHasher.get().encode()).decode())
                newFile.close()
            subprocess.Popen(
                r'explorer /select,".\output\encrypted\"'+nameOfFile+'.txt.aes')
        elif (selectedFile.get() != ''):  # Si l'utilisateur veut chiffrer un fichier
            # On récupère les bytes du fichiers qu'on va chiffrer avec la clé
            with open(selectedFile.get(), 'rb') as willBeEncrypt:
                data = willBeEncrypt.read()
                willBeEncrypt.close()
            # On créer un nouveau fichier (nommé comme l'ancien avec l'extension '.aes')
            with open('./output/encrypted/'+selectedFile.get().split("/")[-1]+'.aes', 'w') as newFile:
                newFile.write(f.encrypt(data).decode())
                newFile.close()
            subprocess.Popen(r'explorer /select,".\output\encrypted\"' +
                             selectedFile.get().split("/")[-1]+'.aes')

# Fonction qui permet le déchiffrement de fichier


def decrypt():
    if (selectedAES.get() != '' and selectedFile.get() != ''):
        # Récupération de la clé AES
        cur = conn.cursor()
        cur.execute("SELECT * FROM aes WHERE name = ?",
                    [selectedAES.get()])

        rows = cur.fetchall()

        aes = rows[0][2]

        f = Fernet(aes.encode())

        # Ouverture du fichier chiffré en 'rb' pour récupérer les bytes
        with open(selectedFile.get(), 'rb') as willBeDecrypt:
            data = willBeDecrypt.read()
            willBeDecrypt.close()
        nameOfNewFile = selectedFile.get().split("/")[-1]
        nameOfNewFile = nameOfNewFile.split(".")
        nameOfNewFile.pop()
        nameOfNewFile = ".".join(nameOfNewFile)

        # Création d'un nouveau fichier en enlevant la dernière extension (.aes par exemple) pour ne laisser que l'extension de base (txt, jpg, etc..)
        with open('./output/decrypted/'+nameOfNewFile, 'wb') as newFile:
            # Ajout des bytes déchiffrés dans le nouveau fichier
            newFile.write(f.decrypt(data))
            newFile.close()
            subprocess.Popen(r'explorer /select,".\output\decrypted\"' +
                             nameOfNewFile)


# Création de la fenêtre
window = tix.Tk()

# Fonction qui ouvre la fenêtre pour l'ajout d'un sel


def createSalt():

    # Fonction qui ajoute le sel en bdd
    def create_salt():

        salt = [entry_name.get(), entry_saltvalue.get()]
        sql = ''' INSERT INTO salt(name,salt)
                VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, salt)
        conn.commit()

        countSalt = 0

        availableSalt.slistbox.listbox.delete(0, tix.END)
        for row in getAllSalt():
            availableSalt.insert(countSalt, row[1])
            ++countSalt

        newSalt.destroy()

        return cur.lastrowid

    # Création et parametrage de la fenêtre
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
        newSalt, text='Ajouter le sel', width=53, command=create_salt).place(x=3, y=70)


actualSaltId = IntVar()
actualSaltName = StringVar()
actualSaltValue = StringVar()

actualSaltId.set(-1)

# Fenêtre qui permet de modifier un sel


def modifySalt():

    if (actualSaltId.get() != -1):
        # Modifie le sel en bdd
        def edit_salt():

            salt = [entry_name.get(), entry_saltvalue.get(),
                    actualSaltId.get()]

            sql = ''' UPDATE salt SET name = ?, salt = ? WHERE id = ?'''
            cur = conn.cursor()
            cur.execute(sql, salt)
            conn.commit()

            editSalt.destroy()

            return cur.lastrowid

        # Création et paramétrage de la fenêtre
        editSalt = Tk()

        editSalt.title("Modification d'un sel")
        editSalt.geometry("385x100")
        editSalt.minsize(385, 100)
        editSalt.config(background='#555555')

        label_name = Label(editSalt, text="Nom", font=(
            "Courrier", 14), bg='#555555', fg='white').place(x=3, y=0)

        entry_name = Entry(editSalt, width=50)
        entry_name.insert(END, actualSaltName.get())
        entry_name.pack()
        entry_name.place(x=78, y=5)

        label_saltValue = Label(editSalt, text="Valeur", font=(
            "Courrier", 14), bg='#555555', fg='white').place(x=3, y=30)

        entry_saltvalue = Entry(editSalt, width=50)
        entry_saltvalue.insert(END, actualSaltValue.get())
        entry_saltvalue.pack()
        entry_saltvalue.place(x=78, y=34)

        button_addSalt = Button(
            editSalt, text='Ajouter le sel', width=53, command=edit_salt).place(x=3, y=70)

# Fonction qui permet de récupérer tout les sels présents en bdd


def getAllSalt():

    cur = conn.cursor()
    cur.execute("SELECT * FROM salt")

    rows = cur.fetchall()

    print("bonjour")

    for row in rows:
        print(row)

    return rows

# Fonction qui permet d'afficher la fenêtre de gestion des sels


def openSalt():

    # Création et paramétrage de la fenêtre
    saltPanel = Tk()

    saltPanel.title("Sels")
    saltPanel.geometry("500x160")
    saltPanel.minsize(500, 160)
    saltPanel.config(background='#555555')

    # Fonction qui affiche la valeur du sel que l'utilisateur a selectionné
    def printSaltValue(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        cur = conn.cursor()
        cur.execute("SELECT * FROM salt WHERE name = ?", [value])

        rows = cur.fetchall()

        actualSaltId.set(rows[0][0])
        actualSaltName.set(rows[0][1])
        actualSaltValue.set(rows[0][2])

        label_saltValue.config(text=("Valeur : "+rows[0][2]))

    # Fonction qui permet de supprimer un sel de la bdd
    def deleteSalt():
        cur = conn.cursor()
        cur.execute("DELETE FROM salt WHERE id = ?", [actualSaltId.get()])
        conn.commit()
        refreshListOfSalt()

    allSalt = Listbox(saltPanel)
    allSalt.bind('<<ListboxSelect>>', printSaltValue)

    countSalt = 0

    # Fonction qui permet d'actualiser la combobox
    def refreshListOfSalt():
        allSalt.delete(0, END)
        availableSalt.slistbox.listbox.delete(0, tix.END)
        for row in getAllSalt():
            allSalt.insert(countSalt, row[1])
            availableSalt.insert(countSalt, row[1])
            ++countSalt

    allSalt.delete(0, END)
    for row in getAllSalt():
        allSalt.insert(countSalt, row[1])
        ++countSalt

    allSalt.pack()
    allSalt.place(x=0, y=0)

    addSalt = Button(saltPanel, text='Ajouter', width=10,
                     command=createSalt).place(x=125, y=0)

    editSalt = Button(saltPanel, text='Editer', width=10,
                      command=modifySalt).place(x=125, y=25)

    deleteSalt = Button(saltPanel, text='Supprimer', width=10,
                        command=deleteSalt).place(x=125, y=50)

    label_saltValue = Label(saltPanel, text="Selectionnez un nom pour voir la valeur du sel", font=(
        "Courrier", 10), bg='#555555', fg='white', height='1')
    label_saltValue.pack()
    label_saltValue.place(x=125, y=80)

    saltPanel.mainloop()

# Fonction pour faire apparaitre la fenêtre de création / génération de clé AES


def createAES():

    # Fonction pour ajouter la nouvelle clé à la bdd
    def create_AES():

        aes = [entry_AESname.get(), entry_AESvalue.get()]

        if (entry_AESname.get() != '' and entry_AESvalue.get() != ''):

            sql = ''' INSERT INTO aes(name,key)
                    VALUES(?,?) '''
            cur = conn.cursor()
            cur.execute(sql, aes)
            conn.commit()

            newAES.destroy()

            countAES = 0

            availableAES.slistbox.listbox.delete(0, tix.END)
            for row in getAllAES():
                availableAES.insert(countAES, row[1])
                ++countAES

    # Fonction qui permet de générer une clé AES
    def generate_AES():

        key = Fernet.generate_key()

        entry_AESvalue.delete(0, END)
        entry_AESvalue.insert(END, key.decode())

    # Création et paramétrage de la fenêtre
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
        newAES, text='Ajouter la clé', width=20, command=create_AES).place(x=3, y=70)
    button_generateAES = Button(
        newAES, text='Générer une clé', width=20, command=generate_AES).place(x=170, y=70)


actualAESId = IntVar()
actualAESName = StringVar()
actualAESValue = StringVar()

actualAESId.set(-1)

# Fonction qui permet l'affichage de la fenêtre de modification de la clé


def modifyAES():

    if (actualAESId.get() != -1):
        # Fonction qui permet la modification de la clé dans la bdd
        def edit_aes():

            aes = [entry_name.get(), entry_AESvalue.get(),
                   actualAESId.get()]

            sql = ''' UPDATE aes SET name = ?, key = ? WHERE id = ?'''
            cur = conn.cursor()
            cur.execute(sql, aes)
            conn.commit()

            editAES.destroy()

            return cur.lastrowid

        # Création et paramétrage de la fenêtre
        editAES = Tk()

        editAES.title("Modification d'un sel")
        editAES.geometry("385x100")
        editAES.minsize(385, 100)
        editAES.config(background='#555555')

        label_name = Label(editAES, text="Nom", font=(
            "Courrier", 14), bg='#555555', fg='white').place(x=3, y=0)

        entry_name = Entry(editAES, width=50)
        entry_name.insert(END, actualAESName.get())
        entry_name.pack()
        entry_name.place(x=78, y=5)

        label_AESValue = Label(editAES, text="Valeur", font=(
            "Courrier", 14), bg='#555555', fg='white').place(x=3, y=30)

        entry_AESvalue = Entry(editAES, width=50)
        entry_AESvalue.insert(END, actualAESValue.get())
        entry_AESvalue.pack()
        entry_AESvalue.place(x=78, y=34)

        button_addAES = Button(
            editAES, text='Ajouter le sel', width=53, command=edit_aes).place(x=3, y=70)

# Fonction qui permet de récupérer toutes les clés AES se trouvant dans la bdd


def getAllAES():

    cur = conn.cursor()
    cur.execute("SELECT * FROM aes")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows

# Fonction pour ouvrir la fenêtre de gestion des clés AES


def openAES():

    aesPanel = Tk()

    aesPanel.title("Clés AES")
    aesPanel.geometry("500x160")
    aesPanel.minsize(500, 160)
    aesPanel.config(background='#555555')

    # Fonction qui permet d'afficher la valeur d'une clé AES
    def printAESValue(evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        cur = conn.cursor()
        cur.execute("SELECT * FROM aes WHERE name = ?", [value])

        rows = cur.fetchall()

        actualAESId.set(rows[0][0])
        actualAESName.set(rows[0][1])
        actualAESValue.set(rows[0][2])

        label_AESValue.config(text=("Valeur : "+rows[0][2]))

    # Fonction qui permet de supprimer une clé AES dans la bdd
    def deleteAES():
        cur = conn.cursor()
        cur.execute("DELETE FROM aes WHERE id = ?", [actualAESId.get()])
        conn.commit()
        refreshListOfAES()

    allAES = Listbox(aesPanel)
    allAES.bind('<<ListboxSelect>>', printAESValue)

    countAES = 0

    # Fonction qui permet d'actualiser la combobox des clés AES
    def refreshListOfAES():
        allAES.delete(0, END)
        availableAES.slistbox.listbox.delete(0, tix.END)
        for row in getAllAES():
            allAES.insert(countAES, row[1])
            availableAES.insert(countAES, row[1])
            ++countAES

    for row in getAllAES():
        allAES.insert(countAES, row[1])
        ++countAES

    allAES.pack()
    allAES.place(x=0, y=0)

    addAES = Button(aesPanel, text='Ajouter', width=10,
                    command=createAES).place(x=125, y=0)

    editAES = Button(aesPanel, text='Editer', width=10,
                     command=modifyAES).place(x=125, y=25)

    deleteAES = Button(aesPanel, text='Supprimer',
                       width=10, command=deleteAES).place(x=125, y=50)

    label_AESValue = Label(aesPanel, text="Selectionnez un nom pour voir la clé AES", font=(
        "Courrier", 10), bg='#555555', fg='white', height='1')
    label_AESValue.pack()
    label_AESValue.place(x=125, y=80)

    aesPanel.mainloop()


# Paramétrage de la fenêtre
window.title("NotACrypter")
window.geometry("1100x720")
window.minsize(1100, 720)
window.maxsize(1100, 720)
window.config(background='#555555')

# premier texte
label_title = Label(window, text="Fonction de hashage", font=(
    "Courrier", 14), bg='#555555', fg='white', height='10').place(x=110, y=110)

label_title4 = Label(window, text="Votre sel", font=(
    "Courrier", 14), bg='#555555', fg='white', height='1').place(x=110, y=395)

label_title5 = Label(window, text="Clés AES", font=(
    "Courrier", 14), bg='#555555', fg='white', height='1').place(x=730, y=300)

label_title6 = Label(window, text="Votre hash", font=(
    "Courrier", 14), bg='#555555', fg='white', height='1').place(x=110, y=530)

selectedSalt = StringVar()

availableSalt = tix.ComboBox(
    window, dropdown=1, variable=selectedSalt)
availableSalt.insert(0, "Pas de sel")
for row in getAllSalt():
    availableSalt.insert(row[0], row[1])
availableSalt.pack()
availableSalt.place(x=220, y=400)

selectedAES = StringVar()

availableAES = tix.ComboBox(
    window, dropdown=1, variable=selectedAES)
for row in getAllAES():
    availableAES.insert(row[0], row[1])
availableAES.pack()
availableAES.place(x=830, y=302)

hashAnswer = StringVar()

hashResult = Entry(window, textvariable=hashAnswer, width=65)
hashResult.pack()
hashResult.place(x=115, y=560)

state = IntVar()
state.set(0)

# Fonction qui permet à l'utilisateur de choisir un fichier sur son disque


def mfileopen():
    selectedFile.set(filedialog.askopenfile().name)
    print(selectedFile.get())
    label_file = Label(window, text=selectedFile.get(), font=(
        "Courrier", 10), bg='#555555', fg='white', height='1').place(x=350, y=140)

# Fonction qui permet a l'utilisateur de choisir entre l'utilisation d'un message ou d'un fichier


def switch():
    if (state.get() == 0):
        state.set(1)
    else:
        state.set(0)
    if (state.get() == 1):
        textAHasher.delete(0, END)
        switchButton.config(text="Utiliser un message")
        label_title3.place(x=-100, y=-200)
        textAHasher.place(x=-100, y=-200)
        button.place(x=480, y=110)
        label_title2.place(x=330, y=9)
    else:
        selectedFile.set('')
        switchButton.config(text="Utiliser un fichier")
        label_title3.place(x=450, y=110)
        textAHasher.place(x=600, y=115)
        button.place(x=-100, y=-200)
        label_title2.place(x=-100, y=-200)


label_title3 = Label(window, text="Votre message", font=(
    "Courrier", 14), bg='#555555', fg='white', height='1')
label_title3.place(x=310, y=110)

textAHasher = Entry(window, width=50)
textAHasher.pack()
textAHasher.place(x=460, y=115)

button = Button(window, text="Sélectionner un document", width=30,
                command=mfileopen)
button.place(x=-100, y=-200)
label_title2 = Label(window, text="Votre document", font=(
    "Courrier", 14), bg='#555555', fg='white', height='10')
label_title2.place(x=-100, y=-200)

selectedFile = StringVar()


varGr = StringVar()

title = Label(window, text="NotACrypter", font=(
    "Courrier", 20), bg='#555555', fg='white').place(x=440, y=5)
subtitle = Label(window, text="by Lucas et Alexandre",
                 font=("Courrier", 8), bg='#555555', fg='white').place(x=460, y=40)

switchButton = Button(window, text="Utiliser un document",
                      command=switch, width=30)
switchButton.place(x=410, y=70)

openSalt = Button(window, text="Gérer les sels", width=30,
                  command=openSalt).place(x=800, y=600)

openAES = Button(window, text="Gérer les clés AES", width=30,
                 command=openAES).place(x=800, y=630)

EncryptButton = Button(window, text="Chiffrer", width=20,
                       command=encrypt).place(x=835, y=430)

DecipherButton = Button(window, text="Déchiffrer", width=20,
                        command=decrypt).place(x=835, y=460)

hashing_button = Button(text="Hasher", width=20,
                        command=hashMsg).place(x=125, y=500)

vals = ['sha1', 'sha256', 'sha512', 'md5', 'blake2b']
etiqs = ['SHA-1', 'SHA-256', 'SHA-512', 'MD5', 'Blake2B']
varGr.set(vals[0])
for i in range(5):
    b = Radiobutton(window, variable=varGr,
                    text=etiqs[i], value=vals[i], activebackground="#555555", bg='#555555', activeforeground="white", foreground="white", selectcolor="black")
    b.pack(side='left', expand=1)
    b.place(x=110, y=(20*i)+260)

# Afficher la fenêtre principal
window.mainloop()
