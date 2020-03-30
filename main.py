import hashlib
import sys
import sqlite3
from sqlite3 import Error
from cryptography.fernet import Fernet

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

salt = "jesuisunsel"
hasher = hashlib.sha512()
with open('julesvern2.epub', 'rb') as afile:
    buf = afile.read()
    hasher.update(salt.encode())
    hasher.update(buf)
print(hasher.hexdigest())


def hashMsg(message, algo):
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
        return 'L\'algorithme n\'est pas connu par NotACrypter'
    m.update(message.encode())
    return m.hexdigest()

# print(hashMsg(sys.argv[1], sys.argv[2]))


key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"Oui bonjour")
print(f.decrypt(token))
