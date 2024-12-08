import iaas
import time


root = iaas.login("root", "root")
# iaas.addHost(root, {"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})

a = iaas.login("a", "a")

print(iaas.listVmShares(a, "7fb1b8ca-d742-4715-9741-ddc2643d72be"))