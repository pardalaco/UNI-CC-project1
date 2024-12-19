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
    
def help_user():
    print(f"""
Avaiable host commands:
    - user list [<query>]
    - user add <email> <password>
    - user update <email> <new password>
    - user rm <userId>
          """)

def help_image():
    print(f"""
Avaiable host commands:
    - image ls [<query>]
    - image add <url> <name> <desc>
    - image rm <imgId>
    - image shares <imgId>
    - image share <imgId> <userEmail>
    - image unshare <imgId> <userId>
          """)
    
def help_vms():
    print(f"""
Avaiable host commands:
    - vm ls [<query]
    - vm add <image> [<mem>]
    - vm start <vmId>
    - vm stop <vmId>
    - vm rm <vmId>
    - vm save <vmId> <imgName> <imgDesc>
    - vm shares <vmId>
    - vm share <vmId> <userEmail>
    - vm unshare <vmId> <userId>
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
    - user update <email> <new password>
    - user rm <userId>
    - image ls [<query>]
    - image add <url> <name> <desc>
    - image rm <imgId>
    - image shares <imgId>
    - image share <imgId> <userEmail>
    - image unshare <imgId> <userId>
    - vm ls [<query]
    - vm add <image> [<mem>]
    - vm start <vmId>
    - vm stop <vmId>
    - vm rm <vmId>
    - vm save <vmId> <imgName> <imgDesc>
    - vm shares <vmId>
    - vm share <vmId> <userEmail>
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

            elif cmd[1] == "update":
                if len(cmd) != 4:
                    print("- user update <email> <new password>")
                else:
                    query_value = f"email = '{cmd[2]}'"
                    listUsers = requests.get(f"http://localhost:5000/iaas/users?query={query_value}", 
                        headers={"Authorization": f"{user[1]}"}, 
                        json={})
                    if listUsers.status_code >= 200 and listUsers.status_code < 300:
                        userUpdateId = json.loads(listUsers.text)[0]['id']

                        userUpdate = requests.put(f"http://localhost:5000/iaas/users/{userUpdateId}", 
                            headers={"Authorization": f"'{user[1]}'"}, 
                            json={"password": cmd[3]})
                        if userUpdate.status_code >= 200 and userUpdate.status_code < 300:
                            print("User updated successfully")
                        else:
                            print(f"{Fore.RED}An error occurred while updating the user.{Style.RESET_ALL}")

            elif cmd[1] == "rm":
                if len(cmd) != 3:
                    print("- user rm <userId>")
                else:
                    userDeleted = requests.delete(f"http://localhost:5000/iaas/users/{cmd[2]}", 
                        headers={"Authorization": f"'{user[1]}'"})
                    if userDeleted.status_code >= 200 and userDeleted.status_code < 300:
                        print("User removed successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while removing the user.{Style.RESET_ALL}")
            else: help_user()
        else: help_user()

    elif cmd[0] == "image":
        if len(cmd) > 1:
            if cmd[1] == "ls":
                query_value = ""
                if len(cmd) > 2:
                    query_value = ' '.join(cmd[2:])

                listImgs = requests.get(f"http://localhost:5000/iaas/images?query={query_value}",
                    headers={"Authorization": f"{user[1]}"},
                    json={})
                if listImgs.status_code >= 200 and listImgs.status_code < 300:
                    images = json.loads(listImgs.text)
                    for img in images:
                        print(img)
                else:
                    print(f"{Fore.RED}An error occurred while listing images.{Style.RESET_ALL}")

            elif cmd[1] == "add":
                if len(cmd) != 5:
                    print("- image add <url> <name> <desc>")
                else:
                    print("Adding image...")
                    addImg = requests.post("http://localhost:5000/iaas/images",
                        headers={"Authorization": f"{user[1]}"},
                        json={"url": cmd[2], "img": {"name": cmd[3], "desc": cmd[4]}})
                    if addImg.status_code >= 200 and addImg.status_code < 300:
                        print("Image added successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while adding the image.{Style.RESET_ALL}")

            elif cmd[1] == "rm":
                if len(cmd) != 3:
                    print("- image rm <imgId>")
                else:
                    print("Removing image")
                    rmImg = requests.delete(f"http://localhost:5000/iaas/images/{cmd[2]}",
                        headers={"Authorization": f"{user[1]}"})
                    if rmImg.status_code >= 200 and rmImg.status_code < 300:
                        print("Image removed successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while removing the image.{Style.RESET_ALL}")
            elif cmd[1] == "shares":
                if len(cmd) != 3:
                    print("- image shares <imgId>")
                else:
                    perms = requests.get(f"http://localhost:5000/iaas/images/{cmd[2]}/shares",
                        headers={"Authorization": f"{user[1]}"})
                    if perms.status_code >= 200 and perms.status_code < 300:
                        permissions = json.loads(perms.text)
                        for perm in permissions:
                            print(perm)
                    else:
                        print(f"{Fore.RED}An error occurred while listing shares for the image.{Style.RESET_ALL}")

            elif cmd[1] == "share":
                if len(cmd) != 4:
                    print("- image share <imgId> <userEmail>")
                else:
                    imgShare = requests.post(f"http://localhost:5000/iaas/images/{cmd[2]}/shares",
                        headers={"Authorization": f"{user[1]}"},
                        json={"user": cmd[3]})
                    if imgShare.status_code >= 200 and imgShare.status_code < 300:
                        print("Image shared successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while sharing the image.{Style.RESET_ALL}")

            elif cmd[1] == "unshare":
                if len(cmd) != 4:
                    print("- image unshare <imgId> <userId>")
                else:
                    imgUnshare = requests.delete(f"http://localhost:5000/iaas/images/{cmd[2]}/shares/{cmd[3]}",
                        headers={"Authorization": f"{user[1]}"})
                    if imgUnshare.status_code >= 200 and imgUnshare.status_code < 300:
                        print("Image unshared successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while unsharing the image.{Style.RESET_ALL}")
            else: help_image()
        else: help_image()

    elif cmd[0] == "vm":
        if len(cmd) > 1:
            if cmd[1] == "ls":
                query_value = ""
                if len(cmd) > 2:
                    query_value = ' '.join(cmd[2:])

                listVms = requests.get(f"http://localhost:5000/iaas/vms?query={query_value}",
                    headers={"Authorization": f"{user[1]}"},
                    json={})
                if listVms.status_code >= 200 and listVms.status_code < 300:
                    vms = json.loads(listVms.text)
                    for vm in vms:
                        print(vm)
                else:
                    print(f"{Fore.RED}An error occurred while listing VMs.{Style.RESET_ALL}")

            elif cmd[1] == "add":
                if len(cmd) < 3 or len(cmd) > 4:
                    print("- vm add <image> [<mem>]")
                else:
                    mem = ""
                    if len(cmd) == 4:
                        mem = cmd[3]
                    print("Adding vm...")
                    addVm = requests.post("http://localhost:5000/iaas/vms",
                        headers={"Authorization": f"{user[1]}"},
                        json={"image": cmd[2], "mem": mem})
                    if addVm.status_code >= 200 and addVm.status_code < 300:
                        print("VM added successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while adding the VM.{Style.RESET_ALL}")

            elif cmd[1] == "start":
                if len(cmd) != 3:
                    print("- vm start <vmId>")
                else:
                    print("Starting vm...")
                    startVm = requests.put(f"http://localhost:5000/iaas/vms/{cmd[2]}",
                        headers={"Authorization": f"{user[1]}"},
                        json={"state": "start"})
                    if startVm.status_code >= 200 and startVm.status_code < 300:
                        print("VM started successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while starting the VM.{Style.RESET_ALL}")

            elif cmd[1] == "stop":
                if len(cmd) != 3:
                    print("- vm stop <vmId>")
                else:
                    print("Stopping vm...")
                    stopVm = requests.put(f"http://localhost:5000/iaas/vms/{cmd[2]}",
                        headers={"Authorization": f"{user[1]}"},
                        json={"state": "stop"})
                    if stopVm.status_code >= 200 and stopVm.status_code < 300:
                        print("VM stopped successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while stopping the VM.{Style.RESET_ALL}")

            elif cmd[1] == "rm":
                if len(cmd) != 3:
                    print("- vm rm <vmId>")
                else:
                    print("Removimg vm...")
                    rmVm = requests.delete(f"http://localhost:5000/iaas/vms/{cmd[2]}",
                        headers={"Authorization": f"{user[1]}"})
                    if rmVm.status_code >= 200 and rmVm.status_code < 300:
                        print("VM removed successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while removing the VM.{Style.RESET_ALL}")

            elif cmd[1] == "save":
                if len(cmd) != 5:
                    print("- vm save <vmId> <imgName> <imgDesc>")
                else:
                    print("Saving image with vm...")
                    saveVm = requests.put(f"http://localhost:5000/iaas/images/{cmd[2]}",
                        headers={"Authorization": f"{user[1]}"},
                        json={"image": {"name": cmd[3], "desc": cmd[4]}})
                    if saveVm.status_code >= 200 and saveVm.status_code < 300:
                        print("VM saved successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while saving the VM.{Style.RESET_ALL}")

            elif cmd[1] == "shares":
                if len(cmd) != 3:
                    print("- vm shares <vmId>")
                else:
                    shares = requests.get(f"http://localhost:5000/iaas/vms/{cmd[2]}/shares",
                        headers={"Authorization": f"{user[1]}"})
                    if shares.status_code >= 200 and shares.status_code < 300:
                        shareList = json.loads(shares.text)
                        for share in shareList:
                            print(share)
                    else:
                        print(f"{Fore.RED}An error occurred while listing shares for the VM.{Style.RESET_ALL}")

            elif cmd[1] == "share":
                if len(cmd) != 4:
                    print("- vm share <vmId> <userEmail>")
                else:
                    vmShare = requests.post(f"http://localhost:5000/iaas/vms/{cmd[2]}/shares",
                        headers={"Authorization": f"{user[1]}"},
                        json={"user": cmd[3]})
                    if vmShare.status_code >= 200 and vmShare.status_code < 300:
                        print("VM shared successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while sharing the VM.{Style.RESET_ALL}")

            elif cmd[1] == "unshare":
                if len(cmd) != 4:
                    print("- vm unshare <vmId> <userId>")
                else:
                    vmUnshare = requests.delete(f"http://localhost:5000/iaas/vms/{cmd[2]}/shares/{cmd[3]}",
                        headers={"Authorization": f"{user[1]}"})
                    if vmUnshare.status_code >= 200 and vmUnshare.status_code < 300:
                        print("VM unshared successfully")
                    else:
                        print(f"{Fore.RED}An error occurred while unsharing the VM.{Style.RESET_ALL}")
            else: help_vms()
        else: help_vms()
            
    elif cmd[0] == "help": help()

    else:
        print("Unknown command. Type 'help' for a list of commands.")