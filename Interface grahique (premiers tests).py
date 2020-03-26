from tkinter import *
from tkinter import filedialog
from tkinter import Radiobutton

# créer une première fenêtre
window = Tk()

# personnamiser cette fenêtre
window.title("NotACrypter")
window.geometry("1080x720")
window.minsize(800, 450)
window.config(background='#555555')

# premier texte
label_title = Label(window, text="Fonction de hashage", font=(
    "Courrier", 14), bg='#555555', fg='white', height='10').place(x=5, y=-95)
# label_title.pack()

label_title2 = Label(window, text="Votre document", font=(
    "Courrier", 14), bg='#555555', fg='white', height='10').place(x=110, y=275)
# label_title.pack()


def mfileopen():
    file1 = filedialog.askopenfile()
    label_file = Label(window, text=file1, font=(
        "Courrier", 10), bg='#555555', fg='white', height='10').place(x=550, y=305)


button = Button(text="Sélectionner un document", width=30,
                command=mfileopen).place(x=300, y=377)

var = IntVar()

check = Checkbutton(window, text="SHA-1", variable=var,
                    font=("Courrier", 10), bg='#555555', fg='white')
check.place(x=275, y=175)
check2 = Checkbutton(window, text="SHA-256", variable=var,
                     font=("Courrier", 10), bg='#555555', fg='white')
check2.place(x=375, y=175)
check3 = Checkbutton(window, text="SHA-512", variable=var,
                     font=("Courrier", 10), bg='#555555', fg='white')
check3.place(x=475, y=175)
check4 = Checkbutton(window, text="MD5", variable=var,
                     font=("Courrier", 10), bg='#555555', fg='white')
check4.place(x=575, y=175)
check5 = Checkbutton(window, text="Blake2B", variable=var,
                     font=("Courrier", 10), bg='#555555', fg='white')
check5.place(x=675, y=175)

vals = ['sha1', 'sha256', 'sha512', 'md5', 'blake2b']
etiqs = ['SHA-1', 'SHA-256', 'SHA-512', 'MD5', 'Blake2B']
varGr = StringVar()
varGr.set(vals[0])
for i in range(5):
    b = Radiobutton(window, variable=varGr,
                    text=etiqs[i], value=vals[i], activebackground="#555555", bg='#555555', activeforeground="white", foreground="white", selectcolor="black")
    b.pack(side='left', expand=1)
    b.place(x=5, y=(20*i)+30)

# afficher
window.mainloop()
