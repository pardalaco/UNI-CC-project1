import iaas
import time
import core

# iaas.init()

root = iaas.login("root", "root")

# iaas.addHost(root, {"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})
# iaas.addUser(root, {"email": "a", "password": "a"})

# img = iaas.addImage(root, 
#                     "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
#                     {"name": "debian-12", "desc":"debian12"})
# print(f"imgRoot: {img}")


a = iaas.login("a", "a")

# img = iaas.addImage(a, 
#                     "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
#                     {"name": "debian-12.1", "desc":"debian12"})
# print(f"imgUserA: {img}")

# print(iaas.listImages(a))

# time.sleep(15)
# iaas.removeImage(a, img['id'])

# vm = core.addVm({
#     "image":"debian-12"
#     })

# print(iaas.listImages(a))

# vm = iaas.addVm(root, {
#     "image":"2cef3df4-51c9-4e48-8bf9-675e16c6db3e"
#     })

# print(vm)

vm = iaas.addVm(a, {
    "image":"2cef3df4-51c9-4e48-8bf9-675e16c6db3e"
    })

vms = iaas.listVms(a)
print(vms)
# print(iaas.listVms(root))

# iaas.startVm(a, vms[0]['id'])
# print(iaas.listVms(a))
# iaas.stopVm(a, vms[0]['id'])
# print(iaas.listVms(a))

img = iaas.saveVmAsImage(
    a,
    vms[0]['id'],
    {"name": "debian12-2", "desc":"debian12"})
print(img)

iaas.removeVm(a, vms[0]['id'])
print(iaas.listVms(a))


print(iaas.listImages(a))