import iaas
import time
import core

iaas.init()

root = iaas.login("root", "root")

iaas.addHost(root, {"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})
iaas.addUser(root, {"email": "a", "password": "a"})
iaas.addUser(root, {"email": "b", "password": "b"})

img = iaas.addImage(root, 
                    "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
                    {"name": "debian-12", "desc":"debian12"})




# ------- Share Vm

a = iaas.login("a", "a")
b = iaas.login("b", "b")

bUserId = iaas.validateToken(b)['id']

vm = iaas.addVm(root, {
    "image": img['id']
    })


iaas.shareVm(root, vm['id'], bUserId)

time.sleep(5)
print("---- ShareVm")

perms = iaas.listVmShares(root, vm['id'])
print(perms)




iaas.unshareVm(root, vm['id'], bUserId)
print("---- unshareVm")


# ------- Share image

iaas.shareImage(root, img['id'], bUserId)

perms = iaas.listImageShares(root, img['id'])
print(perms)

time.sleep(10)
iaas.unshareImage(root, img['id'], bUserId)











# Vm and imgs

# print("---- AddImage")
# time.sleep(5)


# vm = iaas.addVm(root, {
#     "image": img['id']
#     })
# print("---- AddVm")
# time.sleep(5)


# iaas.removeVm(root, vm['id'])
# print("---- RemoveVm")
# time.sleep(5)

# iaas.removeImage(root, img['id'])

