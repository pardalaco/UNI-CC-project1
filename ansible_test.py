import ansible_runner

r = ansible_runner.interface.run(
        host_pattern = "target",
        inventory=f"target ansible_host={host['addr']}",
        playbook = os.path.abspath(FILE_HOST_ADD),
        extravars={
            "host_user": host['user'],
            "host_password": host['password']}
    )