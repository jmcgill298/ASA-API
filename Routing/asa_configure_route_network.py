from asa_aaa_class import ASAAAA
from asa_routing_class import ASARouting
from asa_interface_functions import used_intfcs_name


def main():
    '''
    The purpose of this module is to configure a new static route on a Cisco ASA.
    The ASAAAA class is used to establish a session, and the ASARouting class is
    used to collect the currently used to POST the new route configuration to the
    ASA. The other functions are used to collect configuration and handle formatting.
    This is similar to a 'route interface_name network subnet_mask gateway' from the
    CLI of a Cisco ASA.

    Print:
        The configuration result: A 201 means the configuration was applied,
        other codes indicate an issue with the request. Failures do print
        the code, reason, and content of the response.

    Example:
        (py3) C:\\asa_api_tests>python asa_configure_static_route.py
        What ASA would you like to modify? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input

        LOGIN STATUS_CODE: 204 OK

        What Network would you like to route? EX 192.168.1.0/24: 192.168.100.0/24
        What is the gateway used to reach this network? 192.168.1.9
        What interface name is used to reach this network?
        ['weblab', 'management', 'securelab', 'lab'] lab

        POST ROUTE CONFIG STATUS_CODE: 201 OK

    '''
    asa = input('What ASA would you like to modify? ')
    login_cred = ASAAAA(asa)
    header = login_cred.asa_login()

    config = config_variables(asa, header)
    route = ASARouting(asa, header=header)
    config_route = route.asa_add_static_route(config['network'], config['gateway'], config['zone'])

    if config_route.ok:
        print("\nPOST ROUTE CONFIG STATUS_CODE: {} OK\n".format(config_route.status_code))
    else:
        print("\nPOST ROUTE CONFIG FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            config_route.status_code, config_route.reason, config_route.content))


def config_variables(asa, header):
    '''
    This function is used to collect the configuration details for the
    route being added, and returns them as a dictionary.

    Args:
        asa: The IP or hostname to be used to reach the desired ASA.
        header: The header to use for providing the authentication token.

    Returns:
        A dictionary of route configuration details.

    '''
    return {
        "network": input('What Network would you like to route? EX 192.168.1.0/24: '),
        "gateway": input('What is the gateway used to reach this network? '),
        "zone": input('What interface name is used to reach this network?\n{} '.format(
            used_intfcs_name(asa, header)))
    }


if __name__ == '__main__':
    main()
