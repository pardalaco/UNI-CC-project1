import core
import sqlite3
import traceback
import time
import cryptocode
import json
import uuid

FILE_DB = "iaas.db"
PASSWORD = "password"

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
        cur.execute("""
        CREATE TABLE IF NOT EXISTS perms(
            user varchar(32), 
            resource varchar(32), 
            type varchar(32)
        )""")
        db.commit()
    except Exception as e:
        print("Error")
    db.close()

    # Gestión de usuarios

def login(email, password):
    print(f"login({email}, {password})")
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        
        cur.execute(f"select * from users where email = '{email}' and password = '{password}'")
        rows = cur.fetchall()
        # print(rows)
        if len(rows) == 0: raise Exception("Wrong autentication")

        data = {
            "user": {
                "id": rows[0][0],
                "email": rows[0][1],
                "admin": rows[0][4]
            },
            "ts": time.time_ns()
        }
        # print(data)
        token = cryptocode.encrypt(json.dumps(data), PASSWORD)
        return token
    except Exception as e:
        traceback.print_exc()
        raise e
    finally: 
        db.commit()
        db.close()

def validateToken(token):
    print(f"validateToken({token})")
    data = cryptocode.decrypt(token, PASSWORD)
    if not data: raise Exception("Invalid token")
    data = json.loads(data)
    # Comprobar que data["ts"] no está caducado
    return data["user"]

def addUser(token, user):
    print(f"addUser()")

    issuser = validateToken(token)
    if not issuser["admin"]: raise Exception("Unautorized")

    if "email" not in user: raise Exception("Missing email")
    if "password" not in user: raise Exception("Missing password")

    if "admin" not in user: user["admin"] = 0
    if "quota" not in user: user["quota"] = "{}"

    user["id"] = str(uuid.uuid4())

    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"""INSERT OR IGNORE INTO users VALUES(
                    '{user['id']}', 
                    '{user['email']}', 
                    '{user['password']}', 
                    '{user['quota']}', 
                    '{user['admin']}'
                    )
                    """)
        del user["password"]
        return user
    except Exception as e:
        traceback.print_exc()
        raise e
    finally: 
        db.commit()
        db.close()


def removeUser(tocken, userId): pass

def updateUsers(tocken, userId, data): pass

def listUsers(token, query = ""): 
    print("listVms()")

    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    
    cur.execute(f'select * from users'+ ("" if query == '' else " WHERE " + query))
    rows = cur.fetchall()

    users = []
    for row in rows:
        user = {
            "id": row[0],
            "email": row[1],
            "quota": json.loads(row[3]),
            "admin": row[4]
        }
        users.append(user)
    con.close()


    return users

# ----------- Hosts

def addHost(token, host):
    issuer = validateToken(token)

    if not issuer["admin"]: raise Exception("Unautorized")

    host = core.addHost(host)

    return host

def listHosts(token, query = ""):
    issuer = validateToken(token)
    return core.listHosts(query)

def removeHost(token, hostId): pass

# ---------- Img

def addImage(token, url, img):
    issuer = validateToken(token)

    img = core.addImage(url, img)

    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""INSERT OR IGNORE INTO perms VALUES(
                        '{issuer['id']}', 
                        '{img['id']}', 
                        'image'
                        )
                        """)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()

    return img


def listImages(token, query = ""):
    issuer = validateToken(token)

    if issuer["admin"]:
        images = core.listImages(query)
    else:

        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms where users = '{issuer['id']}' and type='image'""")
            rows = cur.fetchall()
            ids = [f"{row[1]}" for row in rows]
            if len(query): query += " AND id in(" + ",".join(ids) + ")"
            else: query = "id in(" + ",".join(ids) + ")"
            images = core.listImages(query)
            return images
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()

def removeImage(token, imgId): pass
    
# ---------- Vms