import iaas
import time
iaas.init()

root = iaas.login("root", "root")

try:
    iaas.addHost(root, {"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})

    iaas.addUser(root, {"email": "a", "password": "a"})
except:
    pass
# iaas.addUser(root, {"email": "b", "password": "b"})



s = iaas.listUsers(root)
print(s)

user = iaas.updateUser(root, s[1]['id'], {"password": "b"})
print(user)
s = iaas.listUsers(root)
print(f"update: {s}")

a = iaas.login("a", "b")

img = iaas.addImage(a, 
                    "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
                    {"name": "debian-12.1", "desc":"debian12"})

vm = iaas.addVm(a, {
    "image": img['id']
    })


vm = iaas.addVm(a, {
    "image": img['id']
    })
vm = iaas.addVm(a, {
    "image": img['id']
    })

print("aa")
time.sleep(10)

# print(s[1]['id'])
user = iaas.removeUser(root, s[1]['id'])
print(user)

s = iaas.listUsers(root)
print(s)