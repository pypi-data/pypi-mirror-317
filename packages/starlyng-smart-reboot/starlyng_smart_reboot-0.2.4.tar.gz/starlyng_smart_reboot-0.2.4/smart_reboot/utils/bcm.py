"""bcm.py"""
from typing import List, Tuple
from bcm_connection import BCMServer, execute_bcm_command

def check_bcm_chassis_power_status(servers: List[BCMServer]) -> List[Tuple[BCMServer, str]]:
    """
    Checks the power status of multiple servers.

    Args:
        servers (List[BCMServer]): List of BCMServer objects

    Returns:
        List[Tuple[BCMServer, str]]: List of tuples containing BCMServer objects and power status
    """
    return execute_bcm_command(servers, "chassis power status")

def power_off_bcm_servers(servers: List[BCMServer]) -> List[Tuple[BCMServer, str]]:
    """
    Powers off multiple servers.

    Args:
        servers (List[BCMServer]): List of BCMServer objects

    Returns:
        List[Tuple[BCMServer, str]]: List of tuples containing BCMServer objects and power-off results
    """
    return execute_bcm_command(servers, "chassis power off")

def power_on_bcm_servers(servers: List[BCMServer]) -> List[Tuple[BCMServer, str]]:
    """
    Powers on multiple servers.

    Args:
        servers (List[BCMServer]): List of BCMServer objects

    Returns:
        List[Tuple[BCMServer, str]]: List of tuples containing BCMServer objects and power-on results
    """
    return execute_bcm_command(servers, "chassis power on")

def sel_list_bcm_servers(servers: List[BCMServer]) -> List[Tuple[BCMServer, str]]:
    """
    Lists the System Event Log (SEL) for multiple servers.

    Args:
        servers (List[BCMServer]): List of BCMServer objects

    Returns:
        List[Tuple[BCMServer, str]]: List of tuples containing BCMServer objects and SEL list results
    """
    return execute_bcm_command(servers, "sel list")

def sel_clear_bcm_servers(servers: List[BCMServer]) -> List[Tuple[BCMServer, str]]:
    """
    Clears the System Event Log (SEL) for multiple servers.

    Args:
        servers (List[BCMServer]): List of BCMServer objects

    Returns:
        List[Tuple[BCMServer, str]]: List of tuples containing BCMServer objects and SEL clear results
    """
    return execute_bcm_command(servers, "sel clear")
