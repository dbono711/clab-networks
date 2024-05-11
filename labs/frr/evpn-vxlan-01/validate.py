#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import subprocess
from typing import Dict

from loggerfactory import LoggerFactory

logger = LoggerFactory.get_logger("validate.py", log_level="WARNING")


def validate_interface_status(data: Dict, intf: str, device: str) -> bool:
    """
    Validate the administrative and operational status of a network interface.

    Args:
        data (dict): Dictionary containing status information.
        intf (str): Interface identifier.
        switch (str): Switch identifier.

    Returns:
        bool: True if both statuses are 'up', False otherwise.
    """
    status_types = {
        "administrativeStatus": "Administrative",
        "operationalStatus": "Operational",
    }

    for status_type, status_name in status_types.items():
        if data.get(status_type) != "up":
            logger.error(
                f"{status_name} Status for '{intf}' on '{device}' is '{data.get(status_type)}'"
            )
            return False

    return True


def get_interface(intf: str) -> Dict:
    """
    Retrieve information in JSON

    Args:
        intf (str): Interface identifier.

    Returns:
        dict: Interface dictionary.
    """
    reply = subprocess.run(
        [
            "docker",
            "exec",
            "-it",
            "clab-evpn-vxlan-01-leaf01",
            "bash",
            "-c",
            f"vtysh -c 'show interface {intf} json'",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )

    return json.loads(reply.stdout)


def test_interface(device: str, intf: str, peer: str) -> None:
    """
    Test an interface on a device for status

    Args:
        device (str): Device that the interface resides on.
        intf (str): Interface identifier.
        peer (str): Peer that the interface connects to.
    """
    print(f"Checking interface to {peer} on {device}...", end="")
    intf_result = get_interface(intf)

    if intf_result:
        if validate_interface_status(intf_result[intf], intf, device):
            print("[OK]")
        else:
            print("[FAILED]")
    else:
        print(f"ERROR: Interface '{intf}' not found")


def check_interfaces() -> None:
    test_interface("leaf01", "eth3.10", "client1")


def check_network() -> None:
    check_interfaces()


def ping(ip_address: str, container) -> str:
    """
    Pings an ip address in a container.

    Args:
        ip_address (str): Target ip address

    Returns:
        str: Status.
    """
    print(f"Pinging client2 ({ip_address}) from client1 over VNI 110...", end="")
    reply = subprocess.run(
        [
            "docker",
            "exec",
            "-it",
            f"{container}",
            "bash",
            "-c",
            f"ping -c 1 -n {ip_address}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )

    if reply.returncode == 0:
        return "SUCCESS"
    else:
        print("FAILURE! Initiating network validation")
        check_network()


if __name__ == "__main__":
    ping("10.10.1.2", "clab-evpn-vxlan-01-client1")
