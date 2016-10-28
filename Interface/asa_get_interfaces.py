from asa_aaa_class import ASAAAA
from asa_interface_class import ASAInterface


def main():
    '''
    The purpose of this program is to list out an interface's configuration.
    The ASAAAA class is used to establish a session, and the ASAInterface class
    is used to collect the Interface configuration. The other functions are used
    to handle formatting. This is similar to a 'show run interface x/y' from the
    CLI of a Cisco ASA.

    Print:
        The given interface's configuration on the given ASA.

    Example:
        (py3) C:\\asa_api_tests>python asa_get_phys_interfaces.py
        What ASA do you want to view? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input

        LOGIN STATUS_CODE: 204 OK

        Interface GigabitEthernet0/2
         to lab 5K
         weblab
         192.168.1.22 255.255.255.248
         Security: 100
         Speed: auto
         Duplex: auto

        Interface Management0/0

         management
         10.10.10.5 255.255.255.128
         Security: 100
         Speed: auto
         Duplex: auto

        Interface GigabitEthernet0/1
         to lab 5K
         securelab
         192.168.10.1 255.255.255.0
         Security: 40
         Speed: auto
         Duplex: auto

        Interface GigabitEthernet0/0
         to lab 5K
         lab
         192.168.1.14 255.255.255.248
         Security: 20
         Speed: auto
         Duplex: auto

        Available Interfaces are:
         GigabitEthernet0/3
         GigabitEthernet0/4
         GigabitEthernet0/5
         GigabitEthernet0/6
         GigabitEthernet0/7

    '''
    asa = input('What ASA would you like to view? ')
    login_cred = ASAAAA(asa)
    header = login_cred.asa_login()

    asa_intfcs = ASAInterface(asa, header)
    intfcs_config = asa_intfcs.asa_get_phys_interfaces()

    if intfcs_config.ok:
        intfcs_config_json = json.loads(intfcs_config.text)['items']
        print_intfcs(intfcs_config_json)
    else:
        print("GET Interfaces FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            intfcs_config.status_code, intfcs_config.reason, intfcs_config.content))


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


def print_intfcs(intfcs_json):
    '''
    This function is used to print the configured of used interfaces, and lists out
    the interfaces that are currently available.

    Args:
        intfcs_json: The configuration of all interfaces on the ASA in json format.

    Print:
        The interface, description, name-if, security-level, speed, and duplex. It
        prints a list of unused interfaces at the end.

    '''
    avail_intfcs = []
    for intfc_config in intfcs_json:
        if intfc_config["shutdown"]:
            avail_intfcs.append(intfc_config["hardwareID"])
        else:
            intfc = sort_intfc(intfc_config)
            print('\nInterface {}\n {}\n {}\n {}\n Security: {}\n Speed: {}\n Duplex: {}'.format(
                intfc['intfc'], intfc['desc'], intfc['name'], intfc['ip'],
                intfc['level'], intfc['speed'], intfc['duplex']))

    print('\nAvailable Interfaces are: ')
    for intfc in avail_intfcs:
        print(' {}'.format(intfc))


if __name__ == '__main__':
    main()
