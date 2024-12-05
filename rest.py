from flask import Flask, request
import iaas

app = Flask(__name__)

@app.route("/iaas/sessions", methods=["POST"])
def loggin(): 
    creds = request.get_json()
    token = iaas.login(creds["email"], creds["password"])    
    return token


# ----- Hosts
@app.route("/iaas/hosts", methods=["GET"])
def listHosts():
    token = request.headers("Autorization")
    query = request.args.get("query")
    hosts = iaas.listHosts(token, query)
    return hosts

@app.route("/iaas/hosts", methods=["POST"])
def addHost():
    token = request.headers("Autorization")
    host = request.get_json()
    host = iaas.addHost(token, host)
    return host

@app.route("/iaas/hosts/<hostId>", methods=["Put"])
def updateHost(hostId): pass

@app.route("/iaas/hosts/<hostId>", methods=["DELETE"])
def removeHost(hostId): pass


# ----- Users


# ----- Images

# ----- Vms
