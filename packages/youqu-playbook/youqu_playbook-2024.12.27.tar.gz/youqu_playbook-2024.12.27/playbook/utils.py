import os
import re
import sys
import time

from typing import Tuple

from playbook.config import config
from nocmd import RemoteCmd
from funnylog2 import logger


def pre_env():
    empty = "> /dev/null 2>&1"
    os.system("rm -rf ./Pipfile")
    os.system("rm -rf ~/Pipfile")
    os.system("rm -rf .venv")
    os.system("rm -rf ~/.ssh/known_hosts")
    sudo = f"echo '{config.PASSWORD}' | sudo -S"
    if "StrictHostKeyChecking no" not in os.popen("cat /etc/ssh/ssh_config").read():
        os.system(
            f"""{sudo} sed -i "s/#   StrictHostKeyChecking ask/ StrictHostKeyChecking no/g" /etc/ssh/ssh_config {empty}"""
        )
    if os.system(f"sshpass -V {empty}") != 0:
        os.system(f"{sudo} apt update {empty}")
        os.system(f"{sudo} apt install sshpass {empty}")


def check_remote_connected(user, _ip, password, debug: bool = False):
    logger.info(f"Checking remote: {user, _ip, password}")
    if debug:
        return True
    return_code = RemoteCmd(user, _ip, password).remote_run("hostname -I", use_sshpass=True, log_cmd=False)
    if return_code == 0:
        logger.info(f"Remote: {user, _ip, password} connected")
        return True
    return False


def convert_client_to_ip(client: str) -> Tuple[str, str, str]:
    match = re.match(r"^(.+?)@(\d+\.\d+\.\d+\.\d+):{0,1}(.*?)$", client)
    if match:
        user, ip, password = match.groups()
        if not password:
            password = config.PASSWORD
        return user, ip, password
    else:
        raise ValueError("Invalid client format")


def set_playbook_run_exitcode(status):
    if status != 0:
        os.environ["PLAYBOOK_RUN_EXIT_CODE"] = str(status)


def exit_with_playbook_run_exitcode():
    playbook_run_exitcode = os.environ.get("PLAYBOOK_RUN_EXIT_CODE")
    if playbook_run_exitcode is not None and int(playbook_run_exitcode) != 0:
        sys.exit(1)


def are_multisets_equal(l1, l2):
    return all(l1.count(item) == l2.count(item) for item in set(l1)) and len(l1) == len(l2)


def client_reboot(client: str):
    logger.info(f"Rebooting client: {client}")
    user, ip, password = convert_client_to_ip(client)
    RemoteCmd(user, ip, password).remote_sudo_run("reboot", use_sshpass=True, log_cmd=False)


def check_client_enter_desktop(client: str):
    logger.info(f"Checking client: {client} enter desktop")
    user, ip, password = convert_client_to_ip(client)
    stdout, return_code = RemoteCmd(user, ip, password).remote_run(
        "ps -ef | grep -v grep | grep kwin > /dev/null",
        log_cmd=False,
        return_code=True,
        timeout=10,
    )
    if return_code == 0:
        logger.info(f"Client: {client} enter desktop")
        return True
    return False


def reboot_clients(clients: list, reboot: bool = True):
    if not reboot:
        return True
    for client in clients:
        client_reboot(client)
    time.sleep(5)
    for i in range(100):
        for client in clients[::-1]:
            if check_client_enter_desktop(client):
                clients.remove(client)
        if clients:
            time.sleep(2)
        else:
            time.sleep(2)
            logger.info("All clients enter desktop")
            return True
    logger.error("Timeout waiting for clients to enter desktop")
    return False


def get_client_status(host):
    user, ip, password = convert_client_to_ip(host)
    stdout, return_code = RemoteCmd(user, ip, password).remote_run(
        "ps aux | grep -E 'env.sh|pytest' | grep -v grep",
        log_cmd=False,
        return_code=True,
        timeout=10,
    )
    if return_code is None:
        return True
    if return_code == 0:
        return True
    return False



if __name__ == '__main__':
    a = get_client_status("uos@10.20.34.211")
    print(a)
