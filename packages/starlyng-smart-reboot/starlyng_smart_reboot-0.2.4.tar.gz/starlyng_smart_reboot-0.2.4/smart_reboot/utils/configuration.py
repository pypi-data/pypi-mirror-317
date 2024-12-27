"""configuration.py"""
from pathlib import Path
import argparse
import os
import logging
from typing import List, Tuple
from bcm_connection import BCMServer
from ssh_connection import Server, get_hostname, get_ip_for_ssh
from dotenv import load_dotenv
from smart_reboot.utils.conversion import get_port_for_bcm, get_port_for_ssh

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run smart reboot scripts.")
    parser.add_argument('--bcm_servers', type=str, help="Comma-separated list of bcm servers in the format ip:port.")
    parser.add_argument('--bcm_user', type=str, help="BCM username.")
    parser.add_argument('--bcm_pass', type=str, help="BCM password.")
    parser.add_argument('--public_ip', type=str, help="The servers are accessed via public IP addresses.")
    parser.add_argument('--server_mgmt_dir', type=str, help="Smart reboot directory.")
    parser.add_argument('--ssh_base_hostname', type=str, help="Base hostname used for generating server hostnames in the format {hostname}{host_id}")
    parser.add_argument('--ssh_key_path', type=str, help="Path to the SSH key.")
    parser.add_argument('--ssh_user', type=str, help="SSH username.")
    parser.add_argument('--ssh_vlan_id', type=str, help="SSH VLAN ID.")
    parser.add_argument('--vast_api_key', type=str, help="Vast API key.")
    return parser.parse_args()

def load_env_variables(dotenv_path: str = None) -> bool:
    """
    Load environment variables from a .env file if it exists.

    Args:
        dotenv_path (str, optional): Path to the .env file. Defaults to None.

    Returns:
        bool: True if environment variables were loaded successfully, False otherwise.
    """
    if not dotenv_path:
        logging.info("No dotenv_path provided, skipping loading environment variables.")
        return False

    try:
        if not Path(dotenv_path).is_file():
            raise FileNotFoundError(f"The specified dotenv file does not exist: {dotenv_path}")

        return load_dotenv(dotenv_path)

    except (FileNotFoundError, OSError) as error:
        logging.error("Failed to load .env file: %s", error)
        return False

def get_configuration(args: argparse.Namespace) -> Tuple[List[BCMServer], List[Server], str, str]:
    """Retrieve configuration details, prioritizing command-line arguments, then environment variables."""
    config = {
        'bcm_servers': args.bcm_servers or os.getenv('BCM_SERVERS'),
        'bcm_user': args.bcm_user or os.getenv('BCM_USER'),
        'bcm_pass': args.bcm_pass or os.getenv('BCM_PASS'),
        'public_ip': args.public_ip or os.getenv('PUBLIC_IP'),
        'server_mgmt_dir': args.server_mgmt_dir or os.getenv('SERVER_MGMT_DIR'),
        'ssh_base_hostname': args.ssh_base_hostname or os.getenv('SSH_BASE_HOSTNAME'),
        'ssh_key_path': args.ssh_key_path or os.getenv('SSH_KEY_PATH'),
        'ssh_user': args.ssh_user or os.getenv('SSH_USER'),
        'ssh_vlan_id': args.ssh_vlan_id or os.getenv('SSH_VLAN_ID'),
        'vast_api_key': args.vast_api_key or os.getenv('VAST_API_KEY'),
    }

    if any(value is None for value in config.values()):
        raise ValueError(
            "Missing configuration: ensure all required fields are provided "
            "either through command-line arguments or environment variables."
        )

    bcm_servers = [tuple(server.split(':')) for server in config['bcm_servers'].split(',')]
    bcm_servers = [(str(ip), int(port)) for ip, port in bcm_servers]
    public_ip = config['public_ip'].lower() == 'true'

    formatted_bcm_servers = [
        BCMServer(
            bcm_ip=str(ip),
            bcm_user=str(config['bcm_user']),
            bcm_pass=str(config['bcm_pass']),
            bcm_port=int(get_port_for_bcm(ip, port, public_ip)),
            hostname=str(get_hostname(config['ssh_base_hostname'], ip, port, public_ip))
        )
        for ip, port in bcm_servers
    ]

    formatted_ssh_servers = [
        Server(
            public_ip=public_ip,
            hostname=str(get_hostname(config['ssh_base_hostname'], ip, port, public_ip)),
            ip=str(get_ip_for_ssh(ip, config['ssh_vlan_id'], public_ip)),
            ssh_key_path=str(config['ssh_key_path']) if config['ssh_key_path'] else None,
            ssh_port=int(get_port_for_ssh(ip, port, public_ip)),
            ssh_user=str(config['ssh_user']),
            ssh_vlan_id=str(config['ssh_vlan_id'])
        )
        for ip, port in bcm_servers
    ]

    return formatted_bcm_servers, formatted_ssh_servers, config['server_mgmt_dir'], config['vast_api_key']

def load_configuration(dotenv_path: str = None) -> Tuple[List[BCMServer], List[Server], str, str]:
    """
    Loads configuration from command-line arguments, environment variables, and .env file if it exists.

    This function first attempts to load the server configuration, SSH key path, and username
    from command-line arguments. If they are not provided, it falls back to environment variables 
    or the .env file located in the current working directory or a provided path.

    Args:
        dotenv_path (str, optional): Path to the .env file. Defaults to None.

    Returns:
        Tuple[List[BCMServer], List[Server], str, str]: A tuple containing:
            - formatted_bcm_servers (List[BCMServer]): A list of BCMServer objects.
            - formatted_ssh_servers (List[Server]): A list of Server objects.
            - server_mgmt_dir (str): Server management directory.
            - vast_api_key (str): Vast API key.
    """
    args = parse_arguments()
    load_env_variables(dotenv_path=dotenv_path)
    return get_configuration(args)
