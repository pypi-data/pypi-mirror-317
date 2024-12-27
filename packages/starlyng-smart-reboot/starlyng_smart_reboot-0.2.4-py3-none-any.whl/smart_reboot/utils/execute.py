"""execute.py"""
from typing import List
from bcm_connection import BCMServer
from ssh_connection import Server, ping_servers
from smart_reboot.utils.bcm import (
    check_bcm_chassis_power_status,
    power_off_bcm_servers,
    power_on_bcm_servers,
    sel_list_bcm_servers,
    sel_clear_bcm_servers
)
from smart_reboot.utils.file import set_last_reboot, create_bcm_sel_list_logs, write_offline_server_logs
from smart_reboot.utils.connections import get_vast_listed_bcm_server_hostnames

def execute_get_offline_hostnames(ssh_servers: List[Server], vast_api_key: str) -> List[Server]:
    """
    Get a list of offline servers that are listed on Vast.ai.

    Args:
        ssh_servers (List[Server]): A list of all servers.
        vast_api_key (str): Vast API key.

    Returns:
        List[Server]: A list of offline servers that are listed on Vast.ai.
    """
    # Get server hostnames that are unreachable via ping
    unreachable_hostnames = set(ping_servers(ssh_servers))

    # Get BCM server hostnames that are listed on Vast.ai
    vast_listed_bcm_hostnames = get_vast_listed_bcm_server_hostnames(vast_api_key)

    # A server is considered offline if it's both:
    # 1. Unreachable via ping
    # 2. Listed on Vast.ai
    offline_hostnames = set(unreachable_hostnames).intersection(vast_listed_bcm_hostnames)

    # Create lookup set for faster membership testing
    offline_hostnames_set = set(offline_hostnames)
    return [server for server in ssh_servers if server.hostname in offline_hostnames_set]

def execute_smart_reboot_for_offline_hostnames(offline_ssh_servers: List[Server], bcm_servers: List[BCMServer], server_mgmt_dir: str) -> None:
    """
    Perform a smart reboot for offline servers.

    Args:
        offline_ssh_servers (List[Server]): A list of offline servers.
        bcm_servers (List[BCMServer]): A list of BCM servers.
        server_mgmt_dir (str): Directory for server management files.

    Raises:
        ValueError: If server lists don't match or if directory path is invalid
        ConnectionError: If BCM operations fail
    """
    if not server_mgmt_dir:
        raise ValueError("Invalid directory path")

    # Validate server lists match
    offline_ssh_hostnames = {server.hostname for server in offline_ssh_servers}
    bcm_hostnames = {server.hostname for server in bcm_servers}
    if not offline_ssh_hostnames.issubset(bcm_hostnames):
        raise ValueError("Mismatched server lists")

    set_last_reboot(server_mgmt_dir)

    # Get corresponding BCM servers for offline SSH servers
    offline_bcm_servers = [
        bcm_server for bcm_server in bcm_servers
        if bcm_server.hostname in offline_ssh_hostnames
    ]

    # Check power status and power off active servers
    active_offline_servers = [
        server for server, status in check_bcm_chassis_power_status(offline_bcm_servers)
        if status == "Chassis Power is on"
    ]
    if active_offline_servers:
        power_off_bcm_servers(active_offline_servers)

    # Power on all offline servers
    power_on_bcm_servers(offline_bcm_servers)

    # Log errors and clear logs
    logs_for_bcm_servers = sel_list_bcm_servers(offline_bcm_servers)
    create_bcm_sel_list_logs(logs_for_bcm_servers, server_mgmt_dir)
    sel_clear_bcm_servers(offline_bcm_servers)

    # Write journalctl logs for offline servers
    write_offline_server_logs(offline_ssh_servers, server_mgmt_dir)
