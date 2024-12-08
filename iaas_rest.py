import iaas
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# ----------- Users

@app.route("/iaas/sessions", methods=["POST"])
def login():
    """
    Crea una sesión.
    Contenido (JSON): {email,password}
    Resultado (text): token
    """
    print("rest.login()")
    contact = request.get_json()
    return iaas.login(contact['email'], contact['password'])

@app.route("/iaas/users", methods=["POST"])
def addUser():
    """
    Crea un usuario.
    Cabeceras: Authorization: token
    Contenido (JSON): user
    Resultado (JSON): user
    """
    print("rest.addUser()")
    user = request.get_json()
    token = request.headers.get("Authorization")
    return iaas.addUser(token, user)

@app.route("/iaas/users/<userId>", methods=["DELETE"])
def removeUser(userId):
    """
    Elimina un usuario.
    Contenido (JSON): {token}
    """
    print("rest.removeUser()")
    token = request.headers.get("Authorization")
    try:
        user = iaas.removeUser(token, userId)
        return user, 200
    except Exception as e:
        return {"error": e}, 400


@app.route("/iaas/users/<userId>", methods=["PUT"])
def updateUser(userId):
    """
    Actualiza un usuario.
    Contenido (JSON): {token, data}
    """
    print("rest.updateUser()")
    token = request.headers.get("Authorization")
    data = request.get_json()
    try:
        user = iaas.updateUser(token, userId, data)
        return user, 200
    except Exception as e:
        return {"error": e}, 400



@app.route("/iaas/users", methods=["GET"])
def listUsers():
    """
    Lista los usuarios.
    Cabeceras: Authorization: token
    Parámetros: query
    Resultado (JSON): [user]
    """
    print("rest.listUsers()")
    token = request.headers.get("Authorization")
    query = request.args.get("query", "")
    try:
        users = iaas.listUsers(token, query)
        return users, 200
    except Exception as e:
        return {"error": e}, 400



# ----------- Hosts

@app.route("/iaas/hosts", methods=["POST"])
def addHost():
    """
    Crea un host.
    Cabeceras: Authorization: token
    Contenido (JSON): host
    Resultado (JSON): host
    """
    print("rest.addHost()")
    host = request.get_json()
    token = request.headers.get("Authorization")
    return iaas.addHost(token, host)



@app.route("/iaas/hosts", methods=["GET"])
def listHosts(query=""):
    """
    Lista los hosts.
    Cabeceras: Authorization: token
    Parámetros: query (opcional)
    Resultado (JSON): [host]
    """
    print("rest.listHosts()")
    token = request.headers.get("Authorization")
    query = request.args.get("query", "")
    try:
        hosts = iaas.listHosts(token, query)
        return hosts, 200
    except Exception as e:
        return {"error": e}, 400

@app.route("/iaas/hosts/<hostId>", methods=["PUT"])
def updateHost(hostId):
    """
    Actualiza un host.
    Cabeceras: Authorization: token
    Contenido (JSON): data
    Resultado (JSON): host actualizado
    """
    print("rest.updateHost()")
    token = request.headers.get("Authorization")
    data = request.get_json()
    try:
        host = iaas.updateHost(token, hostId, data)
        return host, 200
    except Exception as e:
        return {"error": e}, 400

@app.route("/iaas/hosts/<hostId>", methods=["DELETE"])
def removeHost(hostId):
    """
    Elimina un host.
    Cabeceras: Authorization: token
    Resultado: mensaje de éxito o error
    """
    print("rest.removeHost()")
    # Lógica para eliminar un host
    token = request.headers.get("Authorization")
    try:
        iaas.removeHost(token, hostId)
        return {"succes": "True"}, 200
    except Exception as e:
        return {"error": e}, 400

# ---------- Images

@app.route("/iaas/images", methods=["POST"])
def addImage():
    """
    Crea una imagen.
    Cabeceras: Authorization: token
    Contenido (JSON): image
    Resultado (JSON): image
    """
    print("rest.addImage()")
    token = request.headers.get("Authorization")
    img = request.get_json()
    try:
        image = iaas.addImage(token, img['url'], img['img'])
        return image, 201
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/iaas/images", methods=["GET"])
def listImages():
    """
    Lista las imágenes.
    Cabeceras: Authorization: token
    Parámetros: query (opcional)
    Resultado (JSON): [image]
    """
    print("rest.listImages()")
    token = request.headers.get("Authorization")
    query = request.args.get("query", "")
    try:
        images = iaas.listImages(token, query)
        return images, 200
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/iaas/images/<imgId>", methods=["DELETE"])
def removeImage(imgId):
    """
    Elimina una imagen.
    Cabeceras: Authorization: token
    Resultado: mensaje de éxito o error
    """
    print("rest.removeImage()")
    token = request.headers.get("Authorization")
    try:
        iaas.removeImage(token, imgId)
        return {"success": True}, 200
    except Exception as e:
        return {"error": str(e)}, 400


    
# ---------- Vms


@app.route("/iaas/vms", methods=["POST"])
def addVm():
    """
    Crea una máquina virtual (VM).
    Cabeceras: Authorization: token
    Contenido (JSON): vm
    Resultado (JSON): vm
    """
    print("rest.addVm()")
    token = request.headers.get("Authorization")
    vm = request.get_json()
    try:
        new_vm = iaas.addVm(token, vm)
        return new_vm, 201
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/iaas/vms", methods=["GET"])
def listVms():
    """
    Lista las máquinas virtuales (VMs).
    Cabeceras: Authorization: token
    Parámetros: query (opcional)
    Resultado (JSON): [vm]
    """
    print("rest.listVms()")
    token = request.headers.get("Authorization")
    query = request.args.get("query", "")
    try:
        vms = iaas.listVms(token, query)
        return vms, 200
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/iaas/vms/<vmId>", methods=["DELETE"])
def removeVm(vmId):
    """
    Elimina una máquina virtual (VM).
    Cabeceras: Authorization: token
    Resultado: mensaje de éxito o error
    """
    print("rest.removeVm()")
    token = request.headers.get("Authorization")
    try:
        iaas.removeVm(token, vmId)
        return {"success": True}, 200
    except Exception as e:
        return {"error": str(e)}, 400


def startVm(token:str, vmId:str): pass

def stopVm(token:str, vmId:str): pass

def saveVmAsImage(token:str, vmId:str, img:dict): pass

# ----------- Compartir recursos

def shareVm(token:str, vmId:str, userId:str): pass

def unshareVm(token:str, vmId:str, userId:str): pass

def listVmShares(token:str, vmId:str): pass

def shareImage(token:str, imgId:str, userId:str): pass

def unshareImage(token:str, imgId:str, userId:str): pass

def listImageShares(token:str, imgId:str): pass