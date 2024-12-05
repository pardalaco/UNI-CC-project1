import iaas

# iaas.init()

root = iaas.login("root", "root")


# img = iaas.addImage(root, 
#                     "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
#                     {"name": "debian12", "desc":"debian12"})

# print(img)

listImgs = iaas.listImages(root)
print(listImgs)