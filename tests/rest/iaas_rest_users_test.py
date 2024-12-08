import requests
import iaas
import time
import json

# iaas.init()


root = requests.post("http://localhost:5000/iaas/sessions", json={"email": "root", "password": "root"})
print(root.text)
print()

userInput = time.time()

user = requests.post("http://localhost:5000/iaas/users", 
                  headers={"Authorization": f"'{root.text}'"}, 
                  json={"email": userInput, "password": userInput})

print(user.text)
user = json.loads(user.text)
print(user)
print(user['id'])


userUpdate = requests.put(f"http://localhost:5000/iaas/users/{user['id']}", 
                  headers={"Authorization": f"'{root.text}'"}, 
                  json={"password": "a"})
print("update")
print(userUpdate)


query_value = ""
listUsers = requests.get(f"http://localhost:5000/iaas/users?query={query_value}", 
                  headers={"Authorization": f"{root.text}"}, 
                  json={})
print("update")
print(listUsers.text)



time.sleep(5)


user = requests.delete(f"http://localhost:5000/iaas/users/{user['id']}", 
                  headers={"Authorization": f"'{root.text}'"})
print(user)
