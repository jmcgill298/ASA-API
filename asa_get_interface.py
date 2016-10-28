import json
from asa_aaa_class import ASAAAA
from asa_interface_class import ASAInterface


def main():
    '''
    The purpose of this program is to list out an interface's confiugration.
    The ASAAAA class is used to establish a session, and the ASAInterface class
    is used to collect the Interface configuration. The other functions are used
    to handle formatting. This is similar to a 'show run interface x/y' from the
    CLI of a Cisco ASA.

    Print:
        The given interface's configuration on the given ASA.

    Example:
        (py3) C:\\asa_api_tests>python asa_get_interface.py
        What ASA do you want to view? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input

        LOGIN STATUS_CODE: 204 OK

        What interface would you like to view?
        ['GigabitEthernet0/2', 'Management0/0', 'GigabitEthernet0/1',
        'GigabitEthernet0/0']: GigabitEthernet0/1

        Interface GigabitEthernet0/1
         to lab 5K
         securelab
         192.168.10.1 255.255.255.0
         Security: 40
         Speed: auto
         Duplex: auto

    '''
    asa = input('What ASA would you like to view? ')
    login_cred = ASAAAA(asa)
    header = login_cred.asa_login()

    intfc = input('What interface would you like to view?\n{}: '.format(collected_hardware_id(asa, header)))

    asa_intfc = ASAInterface(asa, header)
    intfc_config = asa_intfc.asa_get_phys_interface(intfc)

    if intfc_config.ok:
        intfc = sort_intfc(json.loads((intfc_config.text)))
        print('\nInterface {}\n {}\n {}\n {}\n Security: {}\n Speed: {}\n Duplex: {}'.format(
            intfc['intfc'], intfc['desc'], intfc['name'], intfc['ip'],
            intfc['level'], intfc['speed'], intfc['duplex']))
    else:
        print("GET Interface FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            intfc_config.status_code, intfc_config.reason, intfc_config.content))


def collected_hardware_id(asa, header):
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

    return used_intfcs


def sort_intfc(config_json):
    '''

    Args:
        config_json: The interface's configuration in json format.

    Returns:
         A dictionary with interesting values; this is used to call desired 'key's for printing.

    '''
    return {
        "intfc": config_json['hardwareID'],
        "desc": config_json['interfaceDesc'],
        "ip": '{} {}'.format(config_json['ipAddress']['ip']['value'], config_json['ipAddress']['netMask']['value']),
        "name": config_json['name'],
        "level": config_json['securityLevel'],
        "speed": config_json['speed'],
        "duplex": config_json['duplex']
    }


if __name__ == '__main__':
    main()
