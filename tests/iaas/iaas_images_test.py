import iaas
import time
import core

iaas.init()

root = iaas.login("root", "root")

iaas.addHost(root, {"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})
iaas.addUser(root, {"email": "a", "password": "a"})

# img = iaas.addImage(root, 
#                     "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
#                     {"name": "debian-12", "desc":"debian12"})
# print(f"imgRoot: {img}")


a = iaas.login("a", "a")

img = iaas.addImage(a, 
                    "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
                    {"name": "debian-12.1", "desc":"debian12"})
# print(f"imgUserA: {img}")

print(iaas.listImages(a))

print("aa")
time.sleep(15)
iaas.removeImage(a, img['id'])


# iaas.removeImage(a, "d44c2a90-0ee9-4280-a642-978de1c3f151")
# iaas.removeImage(root, "d44c2a90-0ee9-4280-a642-978de1c3f151")
# iaas.removeImage(a, "81978acb-fdcc-41a1-b30d-e5dd5e7d5023")