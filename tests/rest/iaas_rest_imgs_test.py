import requests
import time
import json

# iaas.init()


root = requests.post("http://localhost:5000/iaas/sessions", json={"email": "root", "password": "root"})
print(root.text)
root = root.text

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



i = requests.delete(f"http://localhost:5000/iaas/images/{img['id']}", 
                  headers={"Authorization": f"'{root}'"})

query_value = ""
listImgs = requests.get(f"http://localhost:5000/iaas/images?query={query_value}", 
                  headers={"Authorization": f"{root}"}, 
                  json={})
print("list")
print(listImgs)
print(listImgs.text)


