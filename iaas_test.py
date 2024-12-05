import iaas
# iaas.init()

t = iaas.login("root", "root")


iaas.addUser(t, {"email": "b", "password": "b"})

s = iaas.listUsers(t)

print(s)