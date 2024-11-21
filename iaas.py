import core
import sqlite3

FILE_DB = "iaas.db"


def init():
    core.init()

    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id varchar(32),
            email varchar(32),
            password varchar(32),
            quota text,
            admin int
        )
        """)
        cur.execute("INSERT INTO users VALUES('0','root','root','{}',1)")
        db.commit()
    except Exception as e:
        print("Error")
    db.close()