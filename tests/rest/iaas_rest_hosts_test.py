import requests
import iaas
import time
import json

# iaas.init()


root = requests.post("http://localhost:5000/iaas/sessions", json={"email": "root", "password": "root"})
print(root.text)
root = root.text

listH = iaas.listHosts(root)
print(listH)
if listH != []:
    iaas.removeHost(root, listH[0]['id'])

listH = iaas.listHosts(root)
print(listH)

# ------------------- Create host
host = requests.post("http://localhost:5000/iaas/hosts", 
                  headers={"Authorization": f"'{root}'"}, 
                  json={"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})

host = json.loads(host.text)
print(host['id'])


listH = iaas.listHosts(root)
print(listH)
print(listH[0]['id'])




hostupdate = requests.put(f"http://localhost:5000/iaas/hosts/{listH[0]['id']}", 
                  headers={"Authorization": f"'{root}'"}, 
                  json={"addr": "localhost", "user": "alumno", "password": "alumno"})
print("update")



query_value = ""
listHosts = requests.get(f"http://localhost:5000/iaas/hosts?query={query_value}", 
                  headers={"Authorization": f"{root}"}, 
                  json={})
print("list")
print(listHosts)
print(listHosts.text)

time.sleep(5)




# --------------------- Remove Host
h = requests.delete(f"http://localhost:5000/iaas/hosts/{listH[0]['id']}", 
                  headers={"Authorization": f"'{root}'"})
print(h)

# requests.delete(f"http://localhost:5000/iaas/users/407d2f86-8521-4d24-bd7c-255603019844", 
#                   headers={"Authorization": f"'{root}'"})



listH = iaas.listHosts(root)
print(listH)
