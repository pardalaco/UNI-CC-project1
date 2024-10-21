import sqlite3
import ansible_runner
import os
import uuid

FILE_DB = "iaas.db"
FILE_IAAS_INIT = "./plays/iaas_init.yaml"
FILE_HOST_ADD = "./plays/host_add.yaml"
FILE_HOST_RM = "./plays/host_remove.yaml"


def init(): 
    print("init()")

    # Create db
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hosts(
                id varchar(32), 
                addr varchar(32), 
                user varchar(32), 
                password varchar(32)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Vm(
                id varchar(32), 
                image varchar(32), 
                mem int, 
                state varchar(32), 
                host varchar(32)
            )
        """)
        db.commit()
    except Exception as e:
        print("Database alredy exists")
    db.close()

    # Install IaaS
    r = ansible_runner.interface.run(
        host_pattern = "localhost",
        playbook = os.path.abspath(FILE_IAAS_INIT),
        extravars={"iaas_password": "alumnonodo1"}
    )
    if r.status == "failed": raise Exception("Ansible playbook error")


def directory():
    print("destroy()")
    # Hacer lo opuesto de init


    # Eliminamos primero las vm
    

def addHost(host):
    print("addHost()")

    # Check if "host" contains all information necessary
    if "addr" not in host: raise Exception("Missing host addr")
    if "user" not in host: raise Exception("Missing host user")
    if "password" not in host: raise Exception("Missing host password")

    hosts = listHosts(f"addr='{host['addr']}'")
    if len(hosts) > 0: raise Exception("Hosst already exists")

    # Execute the playbook of host_add.yaml
    r = ansible_runner.interface.run(
        host_pattern = "target",
        inventory=f"target ansible_host={host['addr']}",
        playbook = os.path.abspath(FILE_HOST_ADD),
        extravars={
            "host_user": host['user'],
            "host_password": host['password']}
    )
    if r.status == "failed": raise Exception("Ansible playbook error")

    host["id"] = str(uuid.uuid4())

    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    cur.execute(f"insert into hosts values('{host['id']}','{host['addr']}','{host['user']}','{host['password']}')")
    con.commit()
    con.close()

    return host


def removeHost(hostId):
    print("removeHost()")

    hosts = listHosts(f"id='{hostId}'")
    if len(hosts) == 0: raise Exception("Hosst not exists")

    host = hosts[0]
    # print(host)

    # Execute the playbook of host_add.yaml
    r = ansible_runner.interface.run(
        host_pattern = "target",
        inventory=f"target ansible_host={host['addr']}",
        playbook = os.path.abspath(FILE_HOST_RM),
        extravars={
            "host_user": host['user'],
            "host_password": host['password']}
            # "host_password": host['password']} # Error! NO TENEMOS ALMACENADO POR NINGUNA PARTE EL PASSWORD DEL HOST
    )
    if r.status == "failed": raise Exception("Ansible playbook error")

    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()
    cur.execute(f"DELETE FROM hosts WHERE id = '{hostId}';")
    con.commit()
    con.close()



def updateHost(host, data):
    print("updateHost()")

def listHosts(query=''):
    print("listHosts()")

    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()

    cur.execute(f'select * from hosts'+ ("" if query == '' else " WHERE " + query))
    rows = cur.fetchall()
    hosts = []
    for row in rows:
        host = {
            "id": row[0],
            "addr": row[1],
            "user": row[2],
            "password": row[3]            
        }
        hosts.append(host)
    con.close()

    return hosts