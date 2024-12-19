import requests
import sys
import iaas
import os
import iaas
from colorama import Fore, Style
import json


# DEBUG ELIMINAR AL TERMINAR DE DEPURAR
root = requests.post("http://localhost:5000/iaas/sessions", json={"email": "root", "password": "root"})
root = root.text

# listH = iaas.listHosts(root)
# if listH != []:
#     iaas.removeHost(root, listH[0]['id'])



def help_login():
    print(f"""
Usage: python3 cli.py
Avaiable commands:
    - help
    - exit
    - login <email> <password>
          """)

def help_host():
    print(f"""
Avaiable host commands:
    - host ls [<query>]
    - host add <addr> <user> <password>
    - host update <hostId> <addr> <user> <password>
    - host rm <hostId>
          """)

def help():
    print(f"""
Usage: python3 cli.py
Avaiable commands:
    - help
    - exit
    - login <email> <password>
    - host ls [<query>]
    - host add <addr> <user> <password>
    - host update <hostId> <addr> <user> <password>
    - host rm <hostId>
    - user list [<query>]
    - user add <email> <password>
    - user rm <userId>
    - image ls [<query>]
    - image add <url> <name> <desc>
    - image rm <imgId>
    - image shares <imgId>
    - image share <imgId> <userId>
    - image unshare <imgId> <userId>
    - vm ls [<query]
    - vm add <image> [<mem>]
    - vm start <vmId>
    - vm stop <vmId>
    - vm rm <vmId>
    - vm save <vmId> <imgName> <imgDesc>
    - vm shares
    - vm share <vmId> <userId>
    - vm unshare <vmId> <userId>
          """)

def login():
    while True:
        cmd = input("shell> ").split()
        if len(cmd) == 0:
            pass
        elif cmd[0] == "login":
            request = requests.post("http://localhost:5000/iaas/sessions", json={"email": cmd[1], "password": cmd[2]})
            if request.status_code == 500:
                print(f"{Fore.RED}Loggin error, try again.{Style.RESET_ALL}")
            else: 
                return (cmd[1], request.text)

        elif cmd[0] == "exit":
            print("By")
            exit(0)
        else:
            help_login()




# Comprobamos que existe el iaas, de lo contrario lo inicializamos
if not os.path.exists("./iaas.db"):
    iaas.init()

# user = login()
user = ("root", root) # DEBUG
cmd=""
while True:
    cmd = input(f"{user[0]}> ").split()
    if len(cmd) == 0: pass
    elif cmd[0] == "login":
        request = requests.post("http://localhost:5000/iaas/sessions", json={"email": cmd[1], "password": cmd[2]})
        if request.status_code == 500:
            print(f"{Fore.RED}Loggin error, try again.{Style.RESET_ALL}")
        else: 
            user = (cmd[1], request.text)


    elif cmd[0] == "exit":
        print("By")
        exit(0)

    elif cmd[0] == "host":
        if len(cmd) > 1:
            if cmd[1] == "ls":
                query_value = ""
                if len(cmd) > 2:
                    query_value = ' '.join(cmd[2:])

                listHosts = requests.get(f"http://localhost:5000/iaas/hosts?query={query_value}", 
                  headers={"Authorization": f"{user[1]}"}, 
                  json={})
                if listHosts.status_code >= 200 and listHosts.status_code < 300:
                    listHosts = json.loads(listHosts.text)
                    for host in listHosts:
                        print(host)
                else:
                    print(f"{Fore.RED}An error occurred while list hosts.{Style.RESET_ALL}")

            elif cmd[1] == "add":
                if len(cmd) != 5:
                    print("- host add <addr> <user> <password>")
                else:
                    print("Adding host...")
                    host = requests.post("http://localhost:5000/iaas/hosts", 
                        headers={"Authorization": f"'{user[1]}'"}, 
                    json={"addr":cmd[2], "user":cmd[3], "password":cmd[4]})
                    if host.status_code >= 200 and host.status_code < 300:
                        print("Host added successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while adding the host.{Style.RESET_ALL}")

            elif cmd[1] == "rm":
                if len(cmd) != 3:
                    print("- host rm <hostId>")
                else: 
                    print("Removing host...")
                    host = requests.delete(f"http://localhost:5000/iaas/hosts/{cmd[2]}", 
                        headers={"Authorization": f"'{user[1]}'"})
                    if host.status_code >= 200 and host.status_code < 300:
                        print("Host removed successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while removing the host.{Style.RESET_ALL}")
            
            elif cmd[1] == "update":
                if len(cmd) != 6:
                    print("- host update <hostId> <addr> <user> <password>")
                else: 
                    print("Removing host...")
                    host = requests.put(f"http://localhost:5000/iaas/hosts/{cmd[2]}", 
                            headers={"Authorization": f"'{user[1]}'"}, 
                            json={"addr":cmd[3], "user":cmd[4], "password":cmd[5]})
                    
                    if host.status_code >= 200 and host.status_code < 300:
                        print("Host updated successfully")
                    else:
                        print(host.status_code)
                        print(f"{Fore.RED}An error occurred while updated the host.{Style.RESET_ALL}")
            else: help_host()
        else: help_host()


    elif cmd[0] == "user":
        if len(cmd) > 1:
            if cmd[1] == "ls":
                query_value = ""
                if len(cmd) > 2:
                    query_value = ' '.join(cmd[2:])

                listUsers = requests.get(f"http://localhost:5000/iaas/users?query={query_value}", 
                  headers={"Authorization": f"{user[1]}"}, 
                  json={})
                if listUsers.status_code >= 200 and listUsers.status_code < 300:
                    listUsers = json.loads(listUsers.text)
                    for userL in listUsers:
                        print(userL)
                else:
                    print(f"{Fore.RED}An error occurred while list users.{Style.RESET_ALL}")

            elif cmd[1] == "add":
                if len(cmd) != 4:
                    print("- user add <email> <password>")
                else:
                    insertUser = requests.post("http://localhost:5000/iaas/users", 
                        headers={"Authorization": f"'{user[1]}'"}, 
                        json={"email": cmd[2], "password": cmd[3]})
                    if insertUser.status_code >= 200 and insertUser.status_code < 300:
                        print("User added successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while adding the user.{Style.RESET_ALL}")

            elif cmd[1] == "rm":
                pass

    elif cmd[0] == "image":
        if len(cmd) > 1:
            if cmd[1] == "ls":
                pass
            elif cmd[1] == "add":
                pass
            elif cmd[1] == "rm":
                pass
            elif cmd[1] == "shares":
                pass
            elif cmd[1] == "share":
                pass
            elif cmd[1] == "unshare":
                pass

    elif cmd[0] == "vm":
        if len(cmd) > 1:
            if cmd[1] == "ls":
                pass
            elif cmd[1] == "add":
                pass
            elif cmd[1] == "start":
                pass
            elif cmd[1] == "stop":
                pass
            elif cmd[1] == "rm":
                pass
            elif cmd[1] == "save":
                pass
            elif cmd[1] == "shares":
                pass
            elif cmd[1] == "share":
                pass
            elif cmd[1] == "unshare":
                pass

    else:
        print("Unknown command. Type 'help' for a list of commands.")