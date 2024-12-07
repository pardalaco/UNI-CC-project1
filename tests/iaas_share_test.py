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

# ------- Share Vm

# vm = iaas.addVm(a, {
#     "image": img['id']
#     })


# iaas.shareVm(a, vm['id'], bUserId)

# perms = iaas.listVmShares(a, vm['id'])
# print(perms)



# time.sleep(10)

# iaas.unshareVm(a, vm['id'], bUserId)

# ------- Share image

iaas.shareImage(a, img['id'], bUserId)

perms = iaas.listImageShares(a, img['id'])
print(perms)

time.sleep(10)
iaas.unshareImage(a, img['id'], bUserId)
