"""Utility functions for converting between different IP address and port formats."""

from ssh_connection import get_host_id

def get_port_for_bcm(ip: str, port: int, public_ip: bool) -> str:
    """
    Gets the BCM port based on local or public IP addresses.

    Args:
        ip (str): The IP address of the bcm server.
        port (int): The port number of the bcm server.
        public_ip (bool): Whether the server is accessed via public IP.

    Raises:
        ValueError: If the port number is not between 62300 and 62399 for public IPs.
        ValueError: If the IP address is blank.

    Returns:
        str: The BCM port number.
    """
    if not ip:
        raise ValueError("IP address cannot be blank")

    if not public_ip:
        return "623"

    if not 62300 <= port <= 62399:
        raise ValueError(f"Port number must be between 62300 and 62399: port = {port}")

    host_id = get_host_id(ip, port, public_ip)
    return f"623{host_id}"

def get_port_for_ssh(ip: str, port: int, public_ip: bool) -> str:
    """
    Gets the SSH port based on local or public IP addresses.

    Args:
        ip (str): The IP address of the bcm server.
        port (int): The port number of the bcm server.
        public_ip (bool): Whether the server is accessed via public IP.

    Raises:
        ValueError: If the port number is not between 62300 and 62399 for public IPs.
        ValueError: If the IP address is blank.

    Returns:
        str: The SSH port number.
    """
    if not ip:
        raise ValueError("IP address cannot be blank")

    if not public_ip:
        return "22"

    if not 62300 <= port <= 62399:
        raise ValueError(f"Port number must be between 62300 and 62399: port = {port}")

    host_id = get_host_id(ip, port, public_ip)
    return f"22{host_id}"
