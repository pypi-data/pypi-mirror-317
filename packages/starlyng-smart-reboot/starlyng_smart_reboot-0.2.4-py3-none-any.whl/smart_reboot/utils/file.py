"""file.py"""
import logging
import os
import time
from typing import List, Tuple
from ssh_connection import Server, ping_servers, run_command_on_servers

# Core file operations
def get_last_reboot(server_mgmt_dir: str, minutes_since_last_reboot: float) -> bool:
    """
    Check if a reboot has occurred within the specified time frame.

    Args:
        server_mgmt_dir (str): Directory for server management files.
        minutes_since_last_reboot (float): Time threshold in minutes.

    Returns:
        bool: True if a reboot occurred within the specified time, False otherwise.
    """
    file_path = os.path.join(server_mgmt_dir, 'last_reboot')
    logging.info("Checking last reboot file: %s", file_path)

    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_timestamp = float(f.read().strip())
    except (ValueError, IOError) as e:
        logging.error("The file %s does not contain a valid timestamp: %s", file_path, e)
        return False

    time_difference = int((time.time() - file_timestamp) / 60)
    logging.info("Time since last reboot: %s minutes", time_difference)
    return time_difference <= minutes_since_last_reboot

def set_last_reboot(server_mgmt_dir: str) -> None:
    """
    Record the current time as the last reboot time.

    Args:
        server_mgmt_dir (str): Directory for server management files.
    """
    file_path = os.path.join(server_mgmt_dir, 'last_reboot')

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(time.time()))
    except IOError as e:
        logging.error("Error writing to last_reboot file: %s", e)

def _get_log_file_path(server_mgmt_dir: str, server_hostname: str, log_type: str) -> str:
    """
    Get the file path for a log file.

    Args:
        server_mgmt_dir (str): Directory for server management files.
        server_hostname (str): Hostname of the server.
        log_type (str): Type of log file (e.g. 'bcm_sel_list', 'journalctl').

    Returns:
        str: Full file path for the log file.
    """
    reboot_logs_dir = os.path.join(server_mgmt_dir, 'reboot_logs')
    os.makedirs(reboot_logs_dir, exist_ok=True)

    current_date = time.strftime('%Y-%m-%d')
    current_time = int(time.time())

    date_dir = os.path.join(reboot_logs_dir, current_date)
    os.makedirs(date_dir, exist_ok=True)

    file_name = f'{server_hostname}-{current_date}-{current_time}_{log_type}.log'
    file_path = os.path.join(date_dir, file_name)

    return file_path

# BCM SEL list logging
def create_bcm_sel_list_logs(logs_for_bcm_servers: List[Tuple[Server, str]], server_mgmt_dir: str) -> bool:
    """
    Create log files for BCM SEL list data.

    Args:
        logs_for_bcm_servers (List[Tuple[Server, str]]): List of servers and their logs.
        server_mgmt_dir (str): Directory for server management files.

    Returns:
        bool: True if logs are successfully created, False otherwise.
    """
    try:
        for server, logs in logs_for_bcm_servers:
            file_path = _get_log_file_path(server_mgmt_dir, server.hostname, 'bcm_sel_list')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(logs)
        return True

    except OSError as e:
        logging.error("Error creating crash reports: %s", e)
        return False

# Server journalctl logging
def _write_server_journalctl_logs(server: Server, logs: str, server_mgmt_dir: str) -> bool:
    """
    Create log files for journalctl logs.

    Args:
        server (Server): The target server whose logs will be written to disk.
        logs (str): The server logs to write.
        server_mgmt_dir (str): Directory for server management files.

    Returns:
        bool: True if logs are successfully created, False otherwise.
    """
    try:
        file_path = _get_log_file_path(server_mgmt_dir, server.hostname, 'journalctl')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(logs)
        return True

    except OSError as e:
        logging.error("Error creating journalctl logs: %s", e)
        return False

def _process_online_servers(online_servers: List[Server], server_mgmt_dir: str, hours_of_logs: int = 1) -> None:
    """
    Process a list of online servers to get their logs.

    Args:
        servers (List[Server]): List of online servers.
        server_mgmt_dir (str): Directory for server management files.
        hours_of_logs (int, optional): Number of hours of logs to retrieve. Defaults to 1.
    """
    results = run_command_on_servers(online_servers, f"journalctl --since '{hours_of_logs} hours ago'")

    for hostname, result in results.items():
        if result['error']:
            logging.error("Failed to get logs from server %s: %s", hostname, result['error'])
            continue

        logs = result['output']
        server = next(s for s in online_servers if s.hostname == hostname)
        _write_server_journalctl_logs(server, logs, server_mgmt_dir)

def write_offline_server_logs(offline_ssh_servers: List[Server], server_mgmt_dir: str, max_wait_minutes: int = 5) -> None:
    """
    Create journalctl logs for offline SSH servers.

    Args:
        offline_ssh_servers (List[Server]): List of offline SSH servers.
        max_wait_minutes (int, optional): Maximum time to wait for servers to come back online, in minutes. Defaults to 5.
    """
    # Get initial list of unreachable servers
    unreachable_hostnames = set(ping_servers(offline_ssh_servers))
    online_servers = [s for s in offline_ssh_servers if s.hostname not in unreachable_hostnames]
    offline_servers = [s for s in offline_ssh_servers if s.hostname in unreachable_hostnames]

    # Process online servers immediately
    _process_online_servers(online_servers, server_mgmt_dir)

    # Wait for offline servers to come back online
    start_time = time.time()
    max_wait_time = max_wait_minutes * 60  # Convert minutes to seconds

    while offline_servers and (time.time() - start_time) < max_wait_time:
        unreachable = set(ping_servers(offline_servers))
        newly_online = [s for s in offline_servers if s.hostname not in unreachable]

        _process_online_servers(newly_online, server_mgmt_dir)

        for server in newly_online:
            offline_servers.remove(server)

        if offline_servers:
            server_list = ", ".join(s.hostname for s in offline_servers)
            remaining_time = max_wait_time - (time.time() - start_time)
            logging.info("Servers still not reachable: %s. Waiting 30 seconds before retrying (%.1f minutes remaining)",
                          server_list, remaining_time / 60)
            time.sleep(min(30, remaining_time))  # Don't sleep longer than remaining time

    if offline_servers:
        server_list = ", ".join(s.hostname for s in offline_servers)
        logging.error("Servers not reachable after %d minutes of attempts: %s", max_wait_minutes, server_list)
