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
    """
    Inicializa el core del Iaas, invocando la función core.init() y crea
    las tablas necesarias para añadir funcionalidades avanzadas.
    Entre otras, la tabla users.
    """
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
    """
    Autentica a un usuario. Si la operación tiene éxito, devuelve un
    token cifrado, que contiene al menos el id del usuario
    autenticado y la fecha de autenticación. El resto de operaciones
    de iaas.py debe aceptar como primer parámetro este token.
    """
    
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
    """
    Valida el token especificado. Si la operación tiene éxito
    devuelve la información del usuario autenticado.
    """
    print(f"validateToken()")
    data = cryptocode.decrypt(token, PASSWORD)
    if not data: raise Exception("Invalid token")
    data = json.loads(data)
    # Comprobar que data["ts"] no está caducado
    return data["user"]

def addUser(token, user):
    """
    Crea un nuevo usuario. El parámetro user es un diccionario que
    al menos contiene email y password.
    Esta operación sólo puede ser invocada por un administrador.
    Si la operación tiene éxito, devuelve el usuario creado.
    """
    print(f"addUser()")

    # Comprobamos si el token es valido y los campos son correctos
    issuser = validateToken(token)
    if not issuser["admin"]: raise Exception("Unautorized")

    if "email" not in user: raise Exception("Missing email")
    if "password" not in user: raise Exception("Missing password")

    # Definimos los parametros por defecto al usuario
    if "admin" not in user: user["admin"] = 0
    if "quota" not in user: user["quota"] = "{}"

    user["id"] = str(uuid.uuid4())

    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        # Verificar si el usuario con el email ya existe
        cur.execute("SELECT * FROM users WHERE email = ?", (user['email'],))
        existing_user = cur.fetchone()
        if existing_user:
            raise Exception("Email already exists")

        # Insertamos el usuario
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


def removeUser(token, userId):
    """
    Elimina el usuario especificado.
    Sólo puede ser invocada por un administrador.
    Podría conllevar la destrucción de todos los recursos asignados
    al usuario.
    """
    print(f"removeUser()")

    # Validar token de usuario
    issuser = validateToken(token)
    if not issuser["admin"]:
        raise Exception("Unauthorized, admin permision required")

    # Conectar a la base de datos
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()

    try:
        # Comprobar si el usuario con el ID proporcionado existe
        cur.execute(f"SELECT * FROM users WHERE id = '{userId}'")
        rows = cur.fetchone()
        if not rows:
            raise Exception("User not found")
        
        # Crear el diccionario del usuario
        user = {
            "id": rows[0],   
            "email": rows[1],
            "admin": rows[4]
        }
        # Destrucción de los recursos asignados al usuario
        # ???

        # Eliminar el usuario de la base de datos
        cur.execute(f"DELETE FROM users WHERE id = '{userId}'")
        db.commit()

        return user

    except Exception as e:
        traceback.print_exc()
        raise e
    
    finally:
        db.close()

def updateUser(token, userId, data):
    """
    Actualiza el usuario especificado.
    Sólo puede ser invocada por un administrador o el propio
    usuario.
    """
    print(f"updateUser()")

    # Validar token de usuario
    issuser = validateToken(token)
    if not issuser["admin"] and issuser["user_id"] != userId:
        raise Exception("Unauthorized")

    # Conectar a la base de datos
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()

    try:
        # Comprobar si el usuario con el ID proporcionado existe
        cur.execute(f"SELECT * FROM users WHERE id = '{userId}'")
        user = cur.fetchone()
        if not user:
            raise Exception("User not found")

        # Construir la consulta SQL de actualización
        set_clause = []

        # Añadir campos a la cláusula SET
        for key, value in data.items():
            if key not in ["id", "email"]:
                set_clause.append(f"'{key}' = '{value}'")
            else:
                raise Exception(f"It is not allowed to change the value {key}")

        # Si no se encuentran campos válidos para actualizar, lanzar una excepción
        if not set_clause:
            raise Exception("No valid fields to update")

        cur.execute(f"""UPDATE users 
                    SET {', '.join(set_clause)} 
                    WHERE id = '{userId}'""")

        db.commit()

        # Devolver los datos actualizados (sin la contraseña)
        cur.execute("SELECT * FROM users WHERE id = ?", (userId,))
        updated_user = cur.fetchone()
        updated_user_dict = {
            "id": updated_user[0],
            "email": updated_user[1],
            "quota": updated_user[3],
            "admin": updated_user[4]
        }

        return updated_user_dict

    except Exception as e:
        traceback.print_exc()
        raise e

    finally:
        db.close()


def listUsers(token, query = ""): 
    """
    Lista los usuarios especificados en el filtro query.
    """
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