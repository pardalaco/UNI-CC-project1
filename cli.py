import requests
import sys
import iaas
import os
import iaas
from colorama import Fore, Style

def help_login():
    print(f"""
Usage: python3 cli.py
Avaiable commands:
    - help
    - exit
    - login <email> <password>
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

user = login()
while True:
    cmd = input(f"{user[0]}> ").split()
    if len(cmd) == 0: pass
    elif cmd[0] == "login":
        pass

    elif cmd[0] == "exit":
        print("By")
        exit(0)

    elif cmd[0] == "whoami":
        pass

    elif cmd[0] == "host":
        if len(cmd) > 1:
            if cmd[1] == "ls":
                pass
            elif cmd[1] == "add":
                pass
            elif cmd[1] == "rm":
                pass

    elif cmd[0] == "user":
        if len(cmd) > 1:
            if cmd[1] == "list":
                pass
            elif cmd[1] == "add":
                pass
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