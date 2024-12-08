import iaas
import core

# core.init()


# core.addHost({"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})

# vm = core.addVm({
#     "image":"debian-12"
#     })

# print(vm)


# img = core.addImage(
#     "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2",
#     {"name": "debian-12", "desc":"debian12"})

# img = core.saveImage(
#     vm['id'],
#     {"name": "debian12-1", "desc":"debian12"})

img = core.saveImage(
    "57b1247b-60c2-413b-8f01-2b22902d089a",
    {"name": "debian12-1", "desc":"debian12"})


print(img)
