"""connections.py"""
import logging
from typing import List
import requests

def get_vast_listed_bcm_server_hostnames(vast_api_key: str) -> List[str]:
    """
    Get a list of BCM servers and their online status from the Vast.ai API.

    Parameters:
    vast_api_key (str): The API key for Vast.ai.

    Returns:
        List[str]: A list of hostnames for BCM servers that are listed on Vast.ai
    """
    url = "https://console.vast.ai/api/v0/machines"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {vast_api_key}'
    }
    timeout_seconds = 10

    try:
        response = requests.get(url, headers=headers, timeout=timeout_seconds)
        response.raise_for_status()
        json_response = response.json()

        listed_bcm_machines = [
            machine for machine in json_response['machines']
            if machine['mobo_name'].startswith("ROMED8") and machine['listed']
        ]

        return [machine['hostname'] for machine in listed_bcm_machines]
    except requests.Timeout:
        logging.error("The request to %s timed out after %s seconds.", url, timeout_seconds)
    except requests.RequestException as e:
        logging.error("An error occurred while fetching data from Vast.ai API: %s", e)

    return []
