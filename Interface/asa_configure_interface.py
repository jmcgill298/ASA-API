from asa_aaa_class import ASAAAA
from asa_interface_class import ASAInterface


def main():
    '''
    The purpose of this program is to configure a new interface on an ASA.
    The ASAAAA class is used to establish a session, and the ASAInterface
    class is used to configure the Interface. The other functions are used
    to handle formatting.

    Print:
        The configuration result: A 201 means the configuration was applied,
        other codes indicate an issue with the request. Failures do print
        the code, reason, and content of the response.

    Example:
        (py3) C:\\asa_api_tests>python asa_configure_interface.py
        What ASA would you like to configure? 10.10.10.5
        What interface would you like to configure? GigabitEthernet0/3
        What is the secuirity level of the interface? 70
        What is the name of the interface? test
        What is the IP address of the interface? 192.168.1.25
        What is the Mask for this address? 255.255.255.248
        Please enter a description? test desc
        What is your username? username
        Enter your password:

        LOGIN STATUS_CODE: 204 OK

        POST INTERFACE CONFIG STATUS_CODE: 204 OK

    '''
    config = config_variables()

    login_cred = ASAAAA(asa=config['asa'])
    header = login_cred.asa_login()

    interface = ASAInterface(config["asa"], header=header)
    config_interface = interface.asa_config_phys_interface(
        config['interface'], config['security_level'], config['name'],
        config['ip_address'], config['net_mask'], config['description']
    )

    if config_interface.ok:
        print("\nPOST INTERFACE CONFIG STATUS_CODE: {} OK\n".format(config_interface.status_code))
    else:
        print("\nPOST INTERFACE CONFIG FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            config_interface.status_code, config_interface.reason, config_interface.content))


def config_variables():
    '''
    This function is used to collect the desired interface's
    configuration as a dictionaary.

    Returns:
        A dictionary of desired configuration parameters and values.

    '''
    return {
        "asa" : input('What ASA would you like to configure? '),
        "interface": input('What interface would you like to configure? '),
        "security_level" : input('What is the secuirity level of the interface? '),
        "name" : input('What is the name of the interface? '),
        "ip_address" : input('What is the IP address of the interface? '),
        "net_mask" : input('What is the Mask for this address? '),
        "description" : input('Please enter a description? ')
    }


if __name__ == '__main__':
    main()
