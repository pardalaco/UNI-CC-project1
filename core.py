import sqlite3
import ansible_runner
import os
import uuid
import random
import shutil
import json
import libvirt
import traceback
from urllib.request import urlretrieve

FILE_DB = "iaas.db"
FILE_IAAS_INIT = "./plays/iaas_init.yaml"
FILE_IAAS_DESTROY = "./plays/iaas_destroy.yaml"
FILE_HOST_ADD = "./plays/host_add.yaml"
FILE_HOST_RM = "./plays/host_remove.yaml"

DIR_IAAS = "/export/iaas"
DIR_IMAGES = os.path.join(DIR_IAAS, "images")
DIR_VMS = os.path.join(DIR_IAAS, "vms")

DIR_HOST_IMAGES = "/mnt/iaas/images"
DIR_HOST_VMS = "/mnt/iaas/vms"

def init(): 
    """
    Inicializa el nodo controlador. Ello implica, al menos:
    1. Inicializar la base de datos SQLite.
    2. Garantizar que el repositorio del IaaS /export/iaas ha sido exportado por NFS.
    Para (2) se recomienda añadir algunas tareas al playbook ./plays/iaas_init.yaml que se
    aseguren que NFS está instalado localmente, y que exporta el repositorio /export/iaas.
    Serán de utilidad los módulos apt, file, lineinfile y systemd. Por ejemplo:
    """
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
            CREATE TABLE IF NOT EXISTS Vms(
                id varchar(32), 
                image varchar(32), 
                mem int, 
                state varchar(32), 
                host varchar(32)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS images(
                id varchar(32), 
                name varchar(32),  
                description text
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
    if r.status == "failed": raise Exception("Ansible playbook error, iaas not inicializated")


def directory():
    """
    Debería de hacer lo opuesto a core.init(). Esta operación destruye el IaaS. Implica mucho
    trabajo de destrucción, en especial cuando el IaaS tenga múltiples hosts y estos tengan
    múltiples máquinas virtuales. Ejecutará el playbook ./plays/iaas_destroy.yaml.
    """
    print("destroy()")

    # Eliminamos todos los hosts
    hosts = listHosts()
    for host in hosts:
        removeHost(host['id'])

    # Ejecutamos el playbook del iaas destroy
    r = ansible_runner.interface.run(
        host_pattern = "localhost",
        playbook = os.path.abspath(FILE_IAAS_DESTROY),
        extravars={"iaas_password": "alumnonodo1"}
    )
    if r.status == "failed": raise Exception("Ansible playbook error, iaas not destroyed.")



# ---------------- Hosts
def addHost(host):
    """
    Añade un nuevo host al IaaS. Antes será necesario preparar al host. Para ello se utilizará
    el playbook ./plays/host_add.yaml. Ya se ha comentado anteriormente qué implica preparar
    a un host. Serán de utilidad los módulos apt (para instalar Libvirt, cliente NFS), file (para
    crear el directorio local de montaje) y mount (para montar el repositorio del IaaS en el
    directorio local).
    Una vez el host haya sido correctamente preparado, será necesario actualizar la base de
    datos
    """
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
    """
    Elimina un host del IaaS. Esto implica dejarlo en su estado original. Se hará uso del
    playbook ./plays/node_remove.yaml, que efectuará las operaciones opuestas a
    ./plays/node_add.yaml.
    Además, si el host dispone de máquinas virtuales, habría que eliminarlas previamente.
    Si la operación tiene éxito, se actualizará la base de datos convenientemente.
    """
    print("removeHost()")


    hosts = listHosts(f"id='{hostId}'")
    if len(hosts) == 0: raise Exception("Hosst not exists")

    host = hosts[0]
    # print(host)

    # Eliminamos las vm antes de remover el host
    
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"SELECT * FROM vms WHERE host='{hostId}'")
        rows = cur.fetchall()
        if len(rows) == 0: raise Exception("Host does not have vms")
        
        for vm in rows:
            removeVm(vm[0])
        
    except Exception as e:
        traceback.print_exc()
    db.close()
    #------------

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

def updateHost(hostId:str, data:str):
    """Permite actualizar los datos del host."""
    print("updateHost()")
    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()

    update_sql = []
    if 'addr' in data:
        update_sql.append(f"addr = '{data['addr']}'")

    if 'user' in data:
        update_sql.append(f"user = '{data['user']}'")

    if 'password' in data:
        update_sql.append(f"password = '{data['password']}'")

    # print(f'''
    #             UPDATE hosts
    #             SET {", ".join(update_sql)}
    #             WHERE id='{hostId}'
    #             ''')

    cur.execute(f'''
                UPDATE hosts
                SET {", ".join(update_sql)}
                WHERE id='{hostId}'
                ''')
    con.commit()
    con.close()

def listHosts(query=''):
    """
    Lista los hosts que forman parte del IaaS. Bastará con consultar la base de datos local. El
    parámetro query permitirá filtrar los resultados. Para simplificar, se podría aprovechar la
    misma sintaxis de SQL (aunque no sea muy seguro ;-)).
    """
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

# ------- VMs
def addVm(vm:dict):
    """
    Crea una nueva máquina virtual en un host.
    Se selecciona un host en el que se debe ejecutar la máquina virtual.
    Se copia la imagen definida en vm[“image”] del directorio /export/iaas/images al directorio /
    export/iaas/vms con un nombre igual a vm[“id”].
    Se lee la plantilla ./template.xml y se modifican las configuraciones específicas de la
    máquina virtual (el id, la mem, el disk, etc.)
    Se crea el dominio con libvirt.defineXML().
    Se guardan los cambios en la base de datos.
    """
    print("addVm()")
    
    # Comprobamos que la entrada sea correcta
    if "image" not in vm: raise Exception("Missing image")
    
    # Select host

    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute("""
            SELECT * FROM hosts
        """)
        rows = cur.fetchall()
        if len(rows) == 0: raise Exception("No available hosts.")
        index = random.randint(0, len(rows)-1)
        host = {
            "id": rows[index][0],
            "addr": rows[index][1],
            "user": rows[index][2]
            }
        print(json.dumps(host))

        # Copy image
        src = os.path.join(DIR_IMAGES, vm["image"] + ".qcow2")
        vm["id"] = str(uuid.uuid4())

        dst = os.path.join(DIR_VMS, vm["id"] + ".qcow2")
        
        shutil.copyfile(src, dst)
        os.chmod(dst, 0o777)
        
        # Configure template
        f = open("template.xml")
        template = f.read()
        f.close()
        
        vm["mem"] = vm["mem"] if "mem" in vm else 256000
        
        template = template.replace("{{NAME}}", vm["id"]).replace("{{DISK}}", os.path.join(DIR_HOST_VMS, vm["id"] + ".qcow2")).replace("{{MEM}}", str(vm["mem"]))
        
        f = open(os.path.join(DIR_VMS, vm["id"] + ".xml"), "wt")
        f.write(template)
        f.close()
        
        # Create domain
        con = libvirt.open(f"qemu+ssh://{host['user']}@{host['addr']}/system")
        dom = con.defineXML(template)
        con.close()
        
        if dom is None: raise Exception("Unable to create vm")
        
        # Save in database
        cur.execute(f"INSERT INTO vms values('{vm['id']}','{vm['image']}','{vm['mem']}','stopped','{host['id']}')")
        db.commit()
        
    except Exception as e:
        traceback.print_exc()
    db.close()
    # print(vm)
    
    return vm

def startVm(vmId:str):
    """
    Arranca la máquina virtual especificada.
    Se busca el dominio con libvirt.lookupByName().
    Se arranca el dominio con libvirt.create().
    Se guardan los cambios en la base de datos.
    """
    print("startVm()")
    
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"SELECT * FROM vms WHERE id='{vmId}'")
        rows = cur.fetchall()
        if len(rows) == 0: raise Exception("Vm not found")
        
        # Comprobar tambien que la maquina no se encuentre en ejecución
        cur.execute(f"""
            SELECT * FROM hosts WHERE id='{rows[0][4]}'
        """)
        rows = cur.fetchall()
        if len(rows) == 0: raise Exception("Vm not found")
        host = {
            "id": rows[0][0],
            "addr": rows[0][1],
            "user": rows[0][2]
            }
        con = libvirt.open(f"qemu+ssh://{host['user']}@{host['addr']}/system")
        dom = con.lookupByName(vmId)
        dom.create()
        con.close()
        
        cur.execute(f"UPDATE vms SET state='running' WHERE id='{vmId}'")
        db.commit()

        
    except Exception as e:
        traceback.print_exc()
    db.close()  

def stopVm(vmId:str):
    """
    Para la máquina virtual especificada.
    Se busca el dominio con libvirt.lookupByName().
    Se para el dominio con libvirt.shutdown().
    Se guardan los cambios en la base de datos.
    """
    print("stopVm()")
    
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"SELECT * FROM vms WHERE id='{vmId}'")
        rows = cur.fetchall()
        if len(rows) == 0: raise Exception("Vm not found")
        
        # Comprobar tambien que la maquina no se encuentre en ejecución
        cur.execute(f"""
            SELECT * FROM hosts WHERE id='{rows[0][4]}'
        """)
        rows = cur.fetchall()
        if len(rows) == 0: raise Exception("Vm not found")
        host = {
            "id": rows[0][0],
            "addr": rows[0][1],
            "user": rows[0][2]
            }
        con = libvirt.open(f"qemu+ssh://{host['user']}@{host['addr']}/system")
        dom = con.lookupByName(vmId)
        dom.destroy()
        con.close()
        
        cur.execute(f"UPDATE vms SET state='stopped' WHERE id='{vmId}'")
        db.commit()

        
    except Exception as e:
        traceback.print_exc()
    db.close()

def removeVm(vmId:str):
    """
    Elimina la máquina virtual especificada.
    Se busca el dominio con libvirt.lookupByName().
    Se para el dominio con libvirt.undefine().
    Se elimina el disco duro virtual de la máquina virtual de /export/iaas/vms.
    Se guardan los cambios en la base de datos.
    """
    print("removeVm()")
    
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"SELECT * FROM vms WHERE id='{vmId}'")
        rows = cur.fetchall()
        if len(rows) == 0: raise Exception("Vm not found")
        
        # Comprobar tambien que la maquina no se encuentre en ejecución
        cur.execute(f"""
            SELECT * FROM hosts WHERE id='{rows[0][4]}'
        """)
        rows = cur.fetchall()
        if len(rows) == 0: raise Exception("Vm not found")
        host = {
            "id": rows[0][0],
            "addr": rows[0][1],
            "user": rows[0][2]
            }
        con = libvirt.open(f"qemu+ssh://{host['user']}@{host['addr']}/system")
        dom = con.lookupByName(vmId)
        
        if dom.isActive():
            print(f"VM {vmId} is running. Stopping it before removal.")
            dom.destroy()

        dom.undefine()
        con.close()
        
        cur.execute(f"DELETE FROM vms WHERE id='{vmId}'")
        db.commit()

        # Delete the image
        img_path = os.path.join(DIR_VMS, vmId + ".qcow2")
        xml_path = os.path.join(DIR_VMS, vmId + ".xml")
        
        os.remove(img_path)
        os.remove(xml_path)
        
    except Exception as e:
        traceback.print_exc()
    db.close()

def listVms(query:str=''): 
    """
    Lista las máquinas virtuales que forman parte del IaaS. Bastará con consultar la base de
    datos local. El parámetro query permitirá filtrar los resultados. Para simplificar, se podría
    aprovechar la misma sintaxis de SQL (aunque no sea muy seguro ;-)).
    """
    print("listVms()")

    con = sqlite3.connect(FILE_DB)
    cur = con.cursor()

    cur.execute(f'select * from vms'+ ("" if query == '' else " WHERE " + query))
    rows = cur.fetchall()
    vms = []
    for row in rows:
        vm = {
            "id": row[0],
            "image": row[1],
            "mem": row[2],
            "state": row[3],
            "host": row[4]
        }
        vms.append(vm)
    con.close()

    return vms

# ------------------- LAB2

def addImage(url, img) -> dict:
    """
    Añade una nueva imagen al IaaS. El parámetro url especifica
    su ubicación origen. El parámetro img es un diccionario que
    contiene al menos los campos name y desc.
    """
    print(f"addImage({url})")

    if "name" not in img: raise Exception("Missing name")
    if "desc" not in img: raise Exception("Missing desc")

    img["id"] = str(uuid.uuid4())

    # copy file
    urlretrieve(url, os.path.join(DIR_IMAGES, img["id"] + ".qcow2"))

    # print(img)
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"insert into images values('{img['id']}', '{img['name']}', '{img['desc']}')")
        db.commit()
    except Exception as e:
        traceback.print_exc()
    db.close()
    return img

def saveImage(vmId, img):
    """
    Crea una nueva imagen a partir de una vm existente. El
    parámetro vmId especifica la vm. El parámetro img es un
    diccionario que contiene al menos los campos name y desc.
    Si la vm está en ejecución, se recomienda pararla previamente,
    para evitar pérdidas de datos en la imagen.
    """
    print(f"saveImage()")

    if "name" not in img: raise Exception("Missing name")
    if "desc" not in img: raise Exception("Missing desc")

    img["id"] = str(uuid.uuid4())

    # Comprobamos la existencia de la vm
    vm = listVms(f"id = '{vmId}'")
    if vm == []: raise Exception(f"Virtual machin {vmId} don't exist")
    else: vm = vm[0]
    print(vm)

    # Comprobamos que la vm este apagada
    if vm['state'] != "stopped":
        stopVm(vmId)

    # Copiado de la iamgen
    imgOrigin = os.path.join(DIR_VMS, vmId  + ".qcow2")
    imgDestination = os.path.join(DIR_IMAGES, img["id"] + ".qcow2")

    shutil.copyfile(imgOrigin, imgDestination)


    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f"insert into images values('{img['id']}', '{img['name']}', '{img['desc']}')")
        db.commit()
    except Exception as e:
        traceback.print_exc()
    db.close()
    return img

def removeImage(imgId:str):
    """
    Elimina la imagen especificada.
    """
    print(f"removeImage({imgId})")

     # Conectar a la base de datos
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        # Comprobar si la imagen existe en la base de datos
        cur.execute(f"select id from images where id = '{imgId}'")
        result = cur.fetchone()
        if not result:
            raise Exception("Image ID not found in database")

        # Eliminar el archivo de imagen
        img_path = os.path.join(DIR_IMAGES, imgId + ".qcow2")
        if os.path.exists(img_path):
            os.remove(img_path)
        else:
            raise Exception(f"Image file not foundin directory {DIR_IMAGES}")

        # Eliminar la entrada de la base de datos
        cur.execute(f"delete from images where id = '{imgId}'")
        db.commit()
    except Exception as e:
        traceback.print_exc()
        raise
    finally:
        db.close()

def listImages(query=""):
    """
    Lista las imágenes que verifican el filtro especificado en query.
    """
    print("listImages()")
    db = sqlite3.connect(FILE_DB)
    cur = db.cursor()
    try:
        cur.execute(f'select * from images'+ ("" if query == '' else " WHERE " + query)+";")
        rows = cur.fetchall()


        images = []
        for row in rows:
            user = {
                "id": row[0],
                "name": row[1],
                "desc": row[2]
            }
            images.append(user)
    except Exception as e:
        traceback.print_exc()
        raise e
    db.close()


    return images