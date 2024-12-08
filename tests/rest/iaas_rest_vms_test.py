import requests
import iaas
import time
import json

# iaas.init()


root = requests.post("http://localhost:5000/iaas/sessions", json={"email": "root", "password": "root"})
print(root.text)
root = root.text


vm = requests.post("http://localhost:5000/iaas/vms", 
                  headers={"Authorization": f"'{root}'"}, 
                  json={"image": "5e2f8822-9839-4d30-9754-1202e2afff65"})
vm = json.loads(vm.text)
print(vm)
print(vm['id'])


query_value = f"id = '{vm['id']}'"
listImgs = requests.get(f"http://localhost:5000/iaas/vms?query={query_value}", 
                  headers={"Authorization": f"{root}"}, 
                  json={})
print("list")
print(listImgs)
print(listImgs.text)

listImgs = requests.put(f"http://localhost:5000/iaas/vms/{vm['id']}", 
                  headers={"Authorization": f"{root}"}, 
                  json={"state": "start"})

query_value = f"id = '{vm['id']}'"
listImgs = requests.get(f"http://localhost:5000/iaas/vms?query={query_value}", 
                  headers={"Authorization": f"{root}"}, 
                  json={})
print("list")
print(listImgs)
print(listImgs.text)


listImgs = requests.put(f"http://localhost:5000/iaas/vms/{vm['id']}", 
                  headers={"Authorization": f"{root}"}, 
                  json={"state": "stop"})

query_value = f"id = '{vm['id']}'"
listImgs = requests.get(f"http://localhost:5000/iaas/vms?query={query_value}", 
                  headers={"Authorization": f"{root}"}, 
                  json={})
print("list")
print(listImgs)
print(listImgs.text)


i = requests.delete(f"http://localhost:5000/iaas/vms/{vm['id']}", 
                  headers={"Authorization": f"'{root}'"})


query_value = f"id = '{vm['id']}'"
listImgs = requests.get(f"http://localhost:5000/iaas/vms?query={query_value}", 
                  headers={"Authorization": f"{root}"}, 
                  json={})
print("list")
print(listImgs)
print(listImgs.text)
