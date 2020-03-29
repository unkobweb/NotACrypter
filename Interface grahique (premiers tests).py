import hashlib
from tkinter import *
from tkinter import filedialog
from tkinter import Radiobutton
from tkinter import tix
import sqlite3
from sqlite3 import Error

database = r"./pythonsqlite.db"

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


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


conn = create_connection(database)

# create tables
if conn is not None:
    # create projects table
    create_table(conn, sql_create_salt_table)

    # create tasks table
    create_table(conn, sql_create_aes_table)
else:
    print("Error! cannot create the database connection.")


def hashMsg():
    sel = selectedSalt.get()

    m = hashlib.new(varGr.get())
    if (sel != "" and sel != "Pas de sel"):
        m.update(sel.encode())
    m.update(textAHasher.get().encode())
    hashAnswer.set("Hash : "+m.hexdigest().upper())


# créer une première fenêtre
window = tix.Tk()


def createSalt():

    def create_salt():

        salt = [entry_name.get(), entry_saltvalue.get()]
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO salt(name,salt)
                VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, salt)
        conn.commit()

        newSalt.destroy()

        return cur.lastrowid

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


def getAllSalt():

    cur = conn.cursor()
    cur.execute("SELECT * FROM salt")

    rows = cur.fetchall()

    print("bonjour")

    for row in rows:
        print(row)

    return rows


def openSalt():

    saltPanel = Tk()

    saltPanel.title("Sels")
    saltPanel.geometry("500x160")
    saltPanel.minsize(500, 160)
    saltPanel.config(background='#555555')

    allSalt = Listbox(saltPanel)

    countSalt = 0

    for row in getAllSalt():
        print(row)

    for row in getAllSalt():
        allSalt.insert(countSalt, row[1])
        ++countSalt
    allSalt.pack()
    allSalt.place(x=0, y=0)

    addSalt = Button(saltPanel, text='Ajouter', width=10,
                     command=createSalt).place(x=125, y=0)

    editSalt = Button(saltPanel, text='Editer', width=10).place(x=125, y=25)

    deleteSalt = Button(saltPanel, text='Supprimer',
                        width=10).place(x=125, y=50)

    saltPanel.mainloop()


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
