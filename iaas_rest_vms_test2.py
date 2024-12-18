import requests
import iaas
import time
import json

# iaas.init()


# root = requests.post("http://localhost:5000/iaas/sessions", json={"email": "root", "password": "root"})
# print(root)
# print(root.text)
# root = root.text



# a = requests.post("http://localhost:5000/iaas/sessions", json={"email": "asd", "password": "asd"})
# print(a)
# print(a.text)

# try:
#     a = iaas.login("asd", "asd")
# except Exception as e:
#     print(e)



a = requests.post("http://localhost:5000/iaas/sessions", json={"email": "asd", "password": "asd"})

if a.status_code == 500:
    print("Error 500 detectado. Detalles:")

else:
    print(f"Respuesta exitosa: {a.status_code}")
    print(a.text)
