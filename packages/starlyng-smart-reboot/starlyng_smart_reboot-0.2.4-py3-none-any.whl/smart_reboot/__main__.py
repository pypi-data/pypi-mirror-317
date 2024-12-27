"""main.py"""
import logging
from typing import List
from ssh_connection import Server
from smart_reboot.utils.configuration import load_configuration
from smart_reboot.utils.execute import execute_get_offline_hostnames, execute_smart_reboot_for_offline_hostnames
from smart_reboot.utils.file import get_last_reboot

def main() -> None:
    """
    Main function to manage server reboots for offline servers.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        # Load configuration
        bcm_servers, ssh_servers, server_mgmt_dir, vast_api_key = load_configuration()
        logging.info("BCM Servers:")
        for bcm, ssh in zip(bcm_servers, ssh_servers):
            logging.info("  BCM Hostname: %s", bcm.hostname)
            logging.info("  BCM: %s:%s", bcm.bcm_ip, bcm.bcm_port)
            logging.info("  SSH Hostname: %s", ssh.hostname)
            logging.info("  SSH: %s:%s", ssh.ip, ssh.ssh_port)
            logging.info("---")
        logging.info("Server Management Directory: %s", server_mgmt_dir)

        # Prevent reboot if recently rebooted
        if get_last_reboot(server_mgmt_dir, minutes_since_last_reboot=5):
            logging.info("Skipping reboot as servers were recently rebooted.")
            return

        # Get offline hostnames
        offline_ssh_servers: List[Server] = execute_get_offline_hostnames(ssh_servers, vast_api_key)
        logging.info("Offline servers: %s", [server.hostname for server in offline_ssh_servers])

        if offline_ssh_servers:
            logging.info("Found %d offline servers. Initiating smart reboot.", len(offline_ssh_servers))
            execute_smart_reboot_for_offline_hostnames(offline_ssh_servers, bcm_servers, server_mgmt_dir)
        else:
            logging.info("No offline servers found. No action needed.")

    except (IOError, ValueError, KeyError) as e:
        logging.error("An error occurred: %s", str(e))

if __name__ == "__main__":
    main()
