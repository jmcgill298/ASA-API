import json
from asa_interface_class import ASAInterface


def used_intfcs_hardware_id(asa, header):
    '''
    This function is used to get the currently used interfaces.

    Args:
        asa: The IP or hostname to be used to reach the desired ASA.
        header: The header to use for providing the authentication token.

    Returns:
        A list of currently used interfaces.

    '''
    intfc_config = ASAInterface(asa, header)
    intfcs = intfc_config.asa_get_phys_interfaces().text
    intfcs_json = json.loads(intfcs)["items"]
    used_intfcs = []
    for intfc in intfcs_json:
        if not intfc["shutdown"]:
            used_intfcs.append(intfc["hardwareID"])

    used_intfcs.reverse()
    return used_intfcs


def used_intfcs_name(asa, header):
    '''This function uses ASAInterface class to collect the Interfaces,
    and returns just the names of used interfaces

    Args:
        asa: The IP or hostname to be used to reach the desired ASA.
        header: The header to use for providing the authentication token.

    Returns:
         A list of currently used interfaces

    '''
    intfc_config = ASAInterface(asa, header)
    intfcs = json.loads(intfc_config.asa_get_phys_interfaces().text)['items']
    used_intfcs = []
    for intfc in intfcs:
        if not intfc["shutdown"]:
            used_intfcs.append(intfc["name"])

    return used_intfcs


def unused_intfcs_hardware_id(asa, header):
    '''
    This function is used to get the currently unused interfaces.

    Args:
        asa: The IP or hostname to be used to reach the desired ASA.
        header: The header to use for providing the authentication token.

    Returns:
        A list of currently unused interfaces.

    '''
    intfc_config = ASAInterface(asa, header)
    intfcs = intfc_config.asa_get_phys_interfaces().text
    intfcs_json = json.loads(intfcs)["items"]
    unused_intfcs = []
    for intfc in intfcs_json:
        if intfc["shutdown"]:
            unused_intfcs.append(intfc["hardwareID"])

    return unused_intfcs
