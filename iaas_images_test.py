import iaas
import core

# iaas.init()

# root = iaas.login("root", "root")


# img = iaas.addImage(root, 
#                     "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
#                     {"name": "debian12", "desc":"debian12"})

# print(img)

# listImgs = iaas.listImages(root)
# print(listImgs)

# image = iaas.removeImage(root, "cf85d53e-bc30-4bd1-86ab-03a89ed555d0")

# User no root
# user = iaas.addUser(root, {"email": "a", "password": "a"})
# print(user)
# user = iaas.login("a", "a")

# img = iaas.addImage(user, 
#                     "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
#                     {"name": "debian12", "desc":"debian12"})

# image = iaas.removeImage(user, "cf85d53e-bc30-4bd1-86ab-03a89ed555d0")
# image = iaas.removeImage(user, "ec581935-8791-407b-aa89-b82d71768360")

core.removeImage("cf85d53e-bc30-4bd1-86ab-03a89ed555d0")