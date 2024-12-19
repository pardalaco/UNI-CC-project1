import requests

import time
import json

# iaas.init()

root = requests.post("http://localhost:5000/iaas/sessions", json={"email": "root", "password": "root"})
print(root.text)
root = root.text


# Creamos una Vm
vm = requests.post("http://localhost:5000/iaas/vms", 
                  headers={"Authorization": f"'{root}'"}, 
                  json={"image": "d177c075-21e0-4e3d-9320-4c271e39b04f"})
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


img = requests.put(f"http://localhost:5000/iaas/images/{vm['id']}", 
                  headers={"Authorization": f"'{root}'"}, 
                  json={"image": {"name": "debian-12", "desc":"debian12"}})

print(img)
print(img.text)