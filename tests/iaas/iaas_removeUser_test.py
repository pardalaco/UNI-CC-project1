import iaas
import time
import core

iaas.init()

root = iaas.login("root", "root")

iaas.addHost(root, {"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})
iaas.addUser(root, {"email": "a", "password": "a"})
iaas.addUser(root, {"email": "b", "password": "b"})

a = iaas.login("a", "a")
b = iaas.login("b", "b")

bUserId = iaas.validateToken(b)['id']

img = iaas.addImage(a, 
                    "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
                    {"name": "debian-12", "desc":"debian12"})

img2 = iaas.addImage(b, 
                    "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
                    {"name": "debian-12", "desc":"debian12"})

# ------- Share image

iaas.shareImage(a, img['id'], bUserId)


# ------- Share Vm

vm = iaas.addVm(a, {
    "image": img['id']
    })

# vm = iaas.addVm(b, {
#     "image": img['id']
#     })


iaas.shareVm(a, vm['id'], bUserId)

print(iaas.listImageShares(a, img['id']))
print(iaas.listVmShares(a, vm['id']))

iaas.removeUser(root, bUserId)