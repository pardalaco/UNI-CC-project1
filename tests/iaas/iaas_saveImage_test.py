import iaas
import time
import core

iaas.init()

root = iaas.login("root", "root")

iaas.addHost(root, {"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})
iaas.addUser(root, {"email": "a", "password": "a"})
iaas.addUser(root, {"email": "b", "password": "b"})





# ------- Share Vm

a = iaas.login("a", "a")
b = iaas.login("b", "b")

img = iaas.addImage(a, 
                    "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
                    {"name": "debian-12", "desc":"debian12"})


vm = iaas.addVm(root, {
    "image": img['id']
    })


img = iaas.saveVmAsImage(root, 
                         vm['id'], 
                         {"name": "debian-12", "desc":"debian12"})
print(img)

