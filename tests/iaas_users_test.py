import iaas
# iaas.init()

root = iaas.login("root", "root")


iaas.addUser(root, {"email": "a", "password": "a"})
# iaas.addUser(root, {"email": "b", "password": "b"})

s = iaas.listUsers(root)
print(s)

user = iaas.updateUser(root, s[1]['id'], {"password": "b"})
print(user)
s = iaas.listUsers(root)
print(f"update: {s}")

# print(s[1]['id'])
user = iaas.removeUser(root, s[1]['id'])
print(user)

s = iaas.listUsers(root)
print(s)