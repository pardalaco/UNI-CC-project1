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
    print("iaas.init()")
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
        cur.execute("""
            INSERT INTO users
            SELECT '0', 'root', 'root', '{}', 1
            WHERE NOT EXISTS (
                SELECT 1 FROM users WHERE id = '0'
            )
        """)

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

# ----------- Users

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
    print(f"iaas.validateToken()")
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
    print(f"iaas.addUser()")

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
    print(f"iaas.removeUser()")

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
            "password": rows[2],
            "admin": rows[4]
        }

        # Destrucción de los recursos asignados al usuario
        userToken = login(user['email'], user['password'])
        #Eliminamos las imagenes
        images = listImages(userToken)
        for image in images:
            removeImage(userToken, image['id'])
        
        # Eliminamos las vms
        vms = listVms(userToken)
        for vm in vms:
            removeVm(userToken, vm['id'])


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
    print(f"iaas.updateUser()")

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
    print("iaas.listVms()")

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
    """
    Un administrador añade un host. Si es administrador, se
    invocará a core.addHost().
    """
    print("iaas.addHost()")
    issuer = validateToken(token)

    if not issuer["admin"]: raise Exception("Unautorized")

    host = core.addHost(host)

    return host

def listHosts(token, query = ""):
    """
    Cualquier usuario puede listar los hosts. Se invocará
    core.listHosts().
    """
    print("iaas.listHosts()")
    issuer = validateToken(token)
    return core.listHosts(query)

def updateHost(token:str, hostId:str, data:dict):
    """
    Un administrador actualiza un host. Si es administrador, se
    invocará core.updateHost().
    """
    print("iaas.updateHost()")
    issuer = validateToken(token)

    if not issuer["admin"]: raise Exception("Unautorized")

    core.updateHost(hostId, data)

def removeHost(token, hostId): 
    """
    Un administrador elimina un host. Si es administrador, se
    invocará a core.removeHost().
    """
    print("iaas.removeHost()")
    issuer = validateToken(token)

    if not issuer["admin"]: raise Exception("Unautorized")

    core.removeHost(hostId)

# ---------- Img

def addImage(token:str, url:str, img:dict) -> dict:
    """
    Un usuario añade una imagen. Para ello, invoca
    core.addImage(). Al finalizar será necesario añadir un nuevo
    permiso del usuario creador sobre la imagen creada.
    """
    print("iaas.addImage()")
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

def removeImage(token:str, imgId:str): 
    """
    Un usuario elimina su imagen. Si el usuario no es
    administrador, será necesario comprobar su permiso sobre la
    imagen. Después invocará core.removeImage(). Deberán
    eliminarse todos los permisos existentes sobre la imagen.
    """
    print("iaas.removeImage()")
    issuer = validateToken(token)


    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""
                        SELECT * 
                        FROM perms
                        WHERE user = '{issuer['id']}' AND resource = '{imgId}' AND type = 'image'
                    """)
            result = cur.fetchall()
            if result == []: raise Exception(f"Error removeImage(search)")
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()

    core.removeImage(imgId)

    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""
                        DELETE FROM perms
                        WHERE user = '{issuer['id']}' AND resource = '{imgId}' AND type = 'image';
                    """)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()

def listImages(token:str, query:str = ""):
    """
    Un usuario lista sus imágenes. Si el usuario no es
    administrador, será necesario obtener sus permisos sobre
    imágenes. Después invocará core.listImages() buscando dichas
    imágenes.
    """
    print("iaas.listImages()")
    issuer = validateToken(token)

    images = None

    if issuer["admin"]:
        images = core.listImages(query)
    else:

        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms where user = '{issuer['id']}' and type='image'""")
            rows = cur.fetchall()
            ids = [f"'{row[1]}'" for row in rows]
            if len(query): query += " AND id in(" + ", ".join(ids) + ")"
            else: query = "id IN (" + ", ".join(ids) + ")"
            images = core.listImages(query)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()
    
    return images

    
# ---------- Vms

def addVm(token:str, vm:dict):
    """
    Un usuario añade una vm a partir de una imagen. Si el usuario
    no es administrador debe tener permisos sobre la imagen
    origen. Si es el caso, entonces se invoca core.addVm(). Al
    finalizar será necesario añadir un nuevo permiso del usuario
    creador sobre la vm creada.
    """
    print("iaas.addVm()")
    issuer = validateToken(token)

    # Comprobar permisos sobre la imagen
    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms WHERE 
                        user = '{issuer['id']}' and
                        resource = '{vm['image']}' and
                        type = 'image';
                        """)
            rows = cur.fetchall()
            if rows == []: raise Exception("You do not have permissions")
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()


    vm = core.addVm(vm)

    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""INSERT OR IGNORE INTO perms VALUES(
                        '{issuer['id']}', 
                        '{vm['id']}', 
                        'vm'
                        )
                        """)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()
    
    return vm

def listVms(token:str, query:str=""):
    """
    Un usuario lista sus vms. Si el usuario no es administrador,
    será necesario obtener sus permisos sobre vms. Después
    invocará core.listVms() buscando dichas vms.
    """
    print("iaas.listVms()")
    issuer = validateToken(token)

    if issuer["admin"]:
        vms = core.listVms(query)
    else:

        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms where user = '{issuer['id']}' and type='vm'""")
            rows = cur.fetchall()
            ids = [f"'{row[1]}'" for row in rows]
            if len(query): query += " AND id in(" + ", ".join(ids) + ")"
            else: query = "id IN (" + ", ".join(ids) + ")"
            vms = core.listVms(query)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()
    
    return vms

def startVm(token:str, vmId:str):
    """
    Un usuario arranca su vm. Si el usuario no es administrador,
    será necesario comprobar su permiso sobre la vm. Después
    invocará core.startVm().
    """
    print("iaas.startVm()")
    issuer = validateToken(token)

    # Comprobamos si existe la vm
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"""SELECT 1 FROM Vms WHERE id = '{vmId}';""")
        rows = cur.fetchall()
        if rows == []: raise Exception("vm don't exist")
    except Exception as e:
        traceback.print_exc()
        raise e
    finally: 
        db.commit()
        db.close()

    # Verificamos los permisos y ejecutamos la función
    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms WHERE 
                        user = '{issuer['id']}' and
                        resource = '{vmId}' and
                        type = 'vm';
                        """)
            rows = cur.fetchall()
            if rows == []: raise Exception("You do not have permissions")
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()
        
    core.startVm(vmId)

def stopVm(token:str, vmId:str):
    """
    Un usuario para su vm. Si el usuario no es administrador, será
    necesario comprobar su permiso sobre la vm. Después
    invocará core.stopVm().
    """
    print("iaas.stopVm()")
    issuer = validateToken(token)

    # Comprobamos si existe la vm
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"""SELECT 1 FROM Vms WHERE id = '{vmId}';""")
        rows = cur.fetchall()
        if rows == []: raise Exception("vm don't exist")
    except Exception as e:
        traceback.print_exc()
        raise e
    finally: 
        db.commit()
        db.close()

    # Verificamos los permisos y ejecutamos la función
    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms WHERE 
                        user = '{issuer['id']}' and
                        resource = '{vmId}' and
                        type = 'vm';
                        """)
            rows = cur.fetchall()
            if rows == []: raise Exception("You do not have permissions")
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()
        
    core.stopVm(vmId)

def removeVm(token:str, vmId:str):
    """
    Un usuario elimina su vm. Si el usuario no es administrador,
    será necesario comprobar su permiso sobre la vm. Después
    invocará core.removeVm(). Deberán eliminarse todos los
    permisos existentes sobre la vm.
    """
    print("iaas.removeVm()")
    issuer = validateToken(token)

    # Comprobamos si existe la vm
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"""SELECT 1 FROM Vms WHERE id = '{vmId}';""")
        rows = cur.fetchall()
        if rows == []: raise Exception("vm don't exist")
    except Exception as e:
        traceback.print_exc()
        raise e
    finally: 
        db.commit()
        db.close()

    # Verificamos los permisos y ejecutamos la función
    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms WHERE 
                        user = '{issuer['id']}' and
                        resource = '{vmId}' and
                        type = 'vm';
                        """)
            rows = cur.fetchall()
            if rows == []: raise Exception("You do not have permissions")
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()
        
    core.removeVm(vmId)

    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""
                        DELETE FROM perms
                        WHERE user = '{issuer['id']}' AND resource = '{vmId}' AND type = 'vm';
                    """)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()

def saveVmAsImage(token:str, vmId:str, img:dict):
    """
    Un usuario guarda su vm como nueva imagen. Si el usuario no
    es administrador, será necesario comprobar su permiso sobre
    la vm. Después invocará core.saveVmAsImage(). Deberá
    añadirse un nuevo permiso del usuario sobre la imagen creada.
    """
    print("iaas.saveVmAsImage()")
    issuer = validateToken(token)

    # Validamos los permisos del usuario
    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms WHERE 
                        user = '{issuer['id']}' and
                        resource = '{vmId}' and
                        type = 'vm';
                        """)
            rows = cur.fetchall()
            if rows == []: raise Exception("You do not have permissions")
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()
    
    img = core.saveImage(vmId, img)
    return img

# ----------- Compartir recursos

def shareVm(token:str, vmId:str, userId:str):
    """
    Un usuario comparte su vm. Si el usuario no es administrador,
    será necesario comprobar su permiso sobre la vm. Después
    creará el permiso especificado.
    """
    print("iaas.shareVm()")
    issuer = validateToken(token)

    # Comprobamos si existe la vm
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"""SELECT 1 FROM Vms WHERE id = '{vmId}';""")
        rows = cur.fetchall()
        if rows == []: raise Exception("vm don't exist")
    except Exception as e:
        traceback.print_exc()
        raise e
    finally: 
        db.commit()
        db.close()

    # Verificamos los permisos y ejecutamos la función
    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms WHERE 
                        user = '{issuer['id']}' and
                        resource = '{vmId}' and
                        type = 'vm';
                        """)
            rows = cur.fetchall()
            if rows == []: raise Exception("You do not have permissions")
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()



    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"""INSERT OR IGNORE INTO perms VALUES(
                    '{userId}', 
                    '{vmId}', 
                    'vm'
                    )
                    """)
    except Exception as e:
        traceback.print_exc()
        raise e
    finally: 
        db.commit()
        db.close()

def unshareVm(token:str, vmId:str, userId:str):
    """
    Un usuario deja de compartir su vm. Si el usuario no es
    administrador, será necesario comprobar su permiso sobre la
    vm. Después eliminará el permiso especificado
    """
    print("iaas.unshareVm()")
    issuer = validateToken(token)

    # Comprobamos si existe la vm
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"""SELECT 1 FROM Vms WHERE id = '{vmId}';""")
        rows = cur.fetchall()
        if rows == []: raise Exception("vm don't exist")
    except Exception as e:
        traceback.print_exc()
        raise e
    finally: 
        db.commit()
        db.close()

    # Verificamos los permisos y ejecutamos la función
    if not issuer["admin"]:
        db = sqlite3.connect(FILE_DB)
        cur = db.cursor()
        try:
            cur.execute(f"""SELECT * FROM perms WHERE 
                        user = '{issuer['id']}' and
                        resource = '{vmId}' and
                        type = 'vm';
                        """)
            rows = cur.fetchall()
            if rows == []: raise Exception("You do not have permissions")
        except Exception as e:
            traceback.print_exc()
            raise e
        finally: 
            db.commit()
            db.close()



    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"""DELETE FROM perms 
                        WHERE user = '{userId}' 
                        AND resource = '{vmId}' 
                        AND type = 'vm'""")
    except Exception as e:
        traceback.print_exc()
        raise e
    finally: 
        db.commit()
        db.close()

def listVmShares(token:str, vmId:str):
    """
    Lista los permisos sobre una vm. Si el usuario no es
    administrador, será necesario comprobar su permiso sobre la
    vm.
    """

def shareImage(token:str, imgId:str, userId:str):
    """
    Un usuario comparte su imagen. Si el usuario no es
    administrador, será necesario comprobar su permiso sobre la
    imagen. Después creará el permiso especificado.
    """

def unshareImage(token:str, imgId:str, userId:str):
    """
    Un usuario deja de compartir su imagen. Si el usuario no es
    administrador, será necesario comprobar su permiso sobre la
    imagen. Después eliminará el permiso especificado.
    """

def listImageShares(token:str, imgId:str):
    """
    Lista los permisos sobre una imagen. Si el usuario no es
    administrador, será necesario comprobar su permiso sobre la
    imagen.
    """