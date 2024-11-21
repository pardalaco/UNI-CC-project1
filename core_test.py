import time
import core
# core.init()

core.addHost({"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})

core.updateHost(core.listHosts()[0]['id'], {"addr":"172.23.184.138", "user":"alumno", "password":"alumnonodo2"})

# core.removeHost(core.listHosts()[0]["id"])

# core.addHost({"addr":"172.23.185.204", "user":"alumno", "password":"alumno"})
# print(core.listHosts())

# print(core.listHosts()[0]['id'])
# core.removeHost(str(core.listHosts()[0]['id']))
# print(core.listHosts())

# core.removeHost("7491c806-ccda-4d0e-a0a9-c17b1b90ec77")


# core.directory()