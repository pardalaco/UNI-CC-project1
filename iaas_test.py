import iaas
iaas.init()

t = iaas.login("root", "root")


iaas.addUser(t, {"email": "a", "password": "a"})

s = iaas.listUsers(t)

print(s)