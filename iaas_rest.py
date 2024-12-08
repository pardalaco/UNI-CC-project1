import iaas
from flask import Flask, request, jsonify

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
def remove_user(userId):
    """
    Elimina un usuario.
    Contenido (JSON): {token}
    """
    print("rest.removeUser()")


@app.route("/iaas/users/<userId>", methods=["PUT"])
def update_user(userId):
    """
    Actualiza un usuario.
    Contenido (JSON): {token, data}
    """
    print("rest.updateUser()")

@app.route("/iaas/users", methods=["GET"])
def list_users():
    """
    Lista los usuarios.
    Cabeceras: Authorization: token
    Parámetros: query
    Resultado (JSON): [user]
    """



# ----------- Hosts

def addHost(token, host):pass

def listHosts(token, query = ""): pass

def updateHost(token:str, hostId:str, data:dict): pass

def removeHost(token, hostId): pass

# ---------- Img

def addImage(token:str, url:str, img:dict) -> dict: pass

def removeImage(token:str, imgId:str): pass

def listImages(token:str, query:str = ""): pass

    
# ---------- Vms

def addVm(token:str, vm:dict): pass

def listVms(token:str, query:str=""): pass

def startVm(token:str, vmId:str): pass

def stopVm(token:str, vmId:str): pass

def removeVm(token:str, vmId:str): pass

def saveVmAsImage(token:str, vmId:str, img:dict): pass

# ----------- Compartir recursos

def shareVm(token:str, vmId:str, userId:str): pass

def unshareVm(token:str, vmId:str, userId:str): pass

def listVmShares(token:str, vmId:str): pass

def shareImage(token:str, imgId:str, userId:str): pass

def unshareImage(token:str, imgId:str, userId:str): pass

def listImageShares(token:str, imgId:str): pass