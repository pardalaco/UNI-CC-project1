import requests
import iaas
import time
import json

# iaas.init()


root = requests.post("http://localhost:5000/iaas/sessions", json={"email": "root", "password": "root"})
print(root.text)
root = root.text

a = requests.post("http://localhost:5000/iaas/sessions", json={"email": "a", "password": "a"})
a = a.text
print(a)

# Creamos una imagen
img = requests.post("http://localhost:5000/iaas/images", 
                  headers={"Authorization": f"'{root}'"}, 
                  json={
                        "url": "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
                        "img": {
                            "name": "debian-12", 
                            "desc":"debian12"
                            }
                    })
img = json.loads(img.text)
print(img)
print(img['id'])


query_value = ""
listImgs = requests.get(f"http://localhost:5000/iaas/images?query={query_value}", 
                  headers={"Authorization": f"{root}"}, 
                  json={})
print("list")
print(listImgs)
print(listImgs.text)


# Compartimos con usuario
imgShare = requests.post(f"http://localhost:5000/iaas/images/{img['id']}/shares", 
                  headers={"Authorization": f"'{root}'"}, 
                  json={"user": "a"})
print(imgShare)

perms = iaas.listImageShares(a, img["id"])
print("share")
print(perms)

# Consulta
query_value = f"id = '{img['id']}'"
listShareVms = requests.get(f"http://localhost:5000/iaas/images?query={query_value}", 
                  headers={"Authorization": f"{root}"})

print(f"listShareImgs {listShareVms.text}")

# Descompartir con usuario
aUserId = iaas.validateToken(a)['id']
print(aUserId)
imgShare = requests.delete(f"http://localhost:5000/iaas/images/{img['id']}/shares/{aUserId}", 
                  headers={"Authorization": f"'{root}'"})
print(imgShare)

perms = iaas.listImageShares(root, img["id"])
print("unshare")
print(perms)


# Eliminamos la imagen
i = requests.delete(f"http://localhost:5000/iaas/images/{img['id']}", 
                  headers={"Authorization": f"'{root}'"})

query_value = ""
listImgs = requests.get(f"http://localhost:5000/iaas/images?query={query_value}", 
                  headers={"Authorization": f"{root}"}, 
                  json={})
print("list")
print(listImgs)
print(listImgs.text)




# -----------------------

# root = requests.post("http://localhost:5000/iaas/sessions", json={"email": "root", "password": "root"})
# print(root.text)
# root = root.text

# img = requests.post("http://localhost:5000/iaas/images", 
#                   headers={"Authorization": f"'{root}'"}, 
#                   json={
#                         "url": "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
#                         "img": {
#                             "name": "debian-12", 
#                             "desc":"debian12"
#                             }
#                     })
# img = json.loads(img.text)
# print(img)
# print(img['id'])


# query_value = ""
# listImgs = requests.get(f"http://localhost:5000/iaas/images?query={query_value}", 
#                   headers={"Authorization": f"{root}"}, 
#                   json={})
# print("list")
# print(listImgs)
# print(listImgs.text)



# i = requests.delete(f"http://localhost:5000/iaas/images/{img['id']}", 
#                   headers={"Authorization": f"'{root}'"})

# query_value = ""
# listImgs = requests.get(f"http://localhost:5000/iaas/images?query={query_value}", 
#                   headers={"Authorization": f"{root}"}, 
#                   json={})
# print("list")
# print(listImgs)
# print(listImgs.text)



# ---------------------------

# listH = iaas.listHosts(root)
# print(listH)
# if listH != []:
#     iaas.removeHost(root, listH[0]['id'])

# listH = iaas.listHosts(root)
# print(listH)

# # ------------------- Create host
# host = requests.post("http://localhost:5000/iaas/hosts", 
#                   headers={"Authorization": f"'{root}'"}, 
#                   json={"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})

# host = json.loads(host.text)
# print(host['id'])


# listH = iaas.listHosts(root)
# print(listH)
# print(listH[0]['id'])




# hostupdate = requests.put(f"http://localhost:5000/iaas/hosts/{listH[0]['id']}", 
#                   headers={"Authorization": f"'{root}'"}, 
#                   json={"addr": "localhost", "user": "alumno", "password": "alumno"})
# print("update")



# query_value = ""
# listHosts = requests.get(f"http://localhost:5000/iaas/hosts?query={query_value}", 
#                   headers={"Authorization": f"{root}"}, 
#                   json={})
# print("list")
# print(listHosts)
# print(listHosts.text)

# time.sleep(5)




# # --------------------- Remove Host
# h = requests.delete(f"http://localhost:5000/iaas/hosts/{listH[0]['id']}", 
#                   headers={"Authorization": f"'{root}'"})
# print(h)

# # requests.delete(f"http://localhost:5000/iaas/users/407d2f86-8521-4d24-bd7c-255603019844", 
# #                   headers={"Authorization": f"'{root}'"})



# listH = iaas.listHosts(root)
# print(listH)

# userInput = time.time()

# user = requests.post("http://localhost:5000/iaas/users", 
#                   headers={"Authorization": f"'{root.text}'"}, 
#                   json={"email": userInput, "password": userInput})

# print(user.text)
# user = json.loads(user.text)
# print(user)
# print(user['id'])


# userUpdate = requests.put(f"http://localhost:5000/iaas/users/{user['id']}", 
#                   headers={"Authorization": f"'{root.text}'"}, 
#                   json={"password": "a"})
# print("update")
# print(userUpdate)


# query_value = ""
# listUsers = requests.get(f"http://localhost:5000/iaas/users?query={query_value}", 
#                   headers={"Authorization": f"{root.text}"}, 
#                   json={})
# print("update")
# print(listUsers.text)



# time.sleep(5)


# user = requests.delete(f"http://localhost:5000/iaas/users/{user['id']}", 
#                   headers={"Authorization": f"'{root.text}'"})
# print(user)

# ---------------------------------------

# a = requests.get("http://localhost:5000/iaas/users", headers={"Authorization": root}, params={})

# print(a)


# iaas.addHost(root, {"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})
# iaas.addUser(root, {"email": "a", "password": "a"})
# iaas.addUser(root, {"email": "b", "password": "b"})

# img = iaas.addImage(root, 
#                     "https://cloud.debian.org/images/cloud/bookworm/20230531-1397/debian-12-generic-amd64-20230531-1397.qcow2", 
#                     {"name": "debian-12", "desc":"debian12"})




# # ------- Share Vm

# a = iaas.login("a", "a")
# b = iaas.login("b", "b")

# bUserId = iaas.validateToken(b)['id']

# vm = iaas.addVm(root, {
#     "image": img['id']
#     })


# iaas.shareVm(root, vm['id'], bUserId)

# time.sleep(5)
# print("---- ShareVm")

# perms = iaas.listVmShares(root, vm['id'])
# print(perms)




# iaas.unshareVm(root, vm['id'], bUserId)
# print("---- unshareVm")


# # ------- Share image

# iaas.shareImage(root, img['id'], bUserId)

# perms = iaas.listImageShares(root, img['id'])
# print(perms)

# time.sleep(10)
# iaas.unshareImage(root, img['id'], bUserId)











# # Vm and imgs

# # print("---- AddImage")
# # time.sleep(5)


# # vm = iaas.addVm(root, {
# #     "image": img['id']
# #     })
# # print("---- AddVm")
# # time.sleep(5)


# # iaas.removeVm(root, vm['id'])
# # print("---- RemoveVm")
# # time.sleep(5)

# # iaas.removeImage(root, img['id'])

