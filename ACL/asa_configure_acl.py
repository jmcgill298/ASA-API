from asa_aaa_class import ASAAAA
from asa_acl_class import ASAACL
from asa_acl_functions import get_acl_last_position
from asa_interface_functions import used_intfcs_name


def main():
    '''
    The purpose of this program is to configure a new line of policy to an
    existing ACL on a Cisco ASA. The ASAAAA class is used to establish a
    session, the ASAInterface class is used to collect the currently used
    interfaces, and the ASAACL class is used to POST the new ACL configuration
    policy. The other functions are used to collect configuration and handle
    formatting. This is similar to an 'access-list acl_name remark remark'
    and 'access-list acl_name extended [permit,deny] source destination
    service log' from the CLI of a Cisco ASA.

    Print:
        The configuration result: A 201 means the configuration was applied,
        other codes indicate an issue with the request. Failures do print
        the code, reason, and content of the response.

    Example:
        (py3) C:\\asa_api_tests>python asa_configure_acl.py
        What ASA would you like to modify? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input

        LOGIN STATUS_CODE: 204 OK

        What interface's policy would you like to modify?
         ['weblab', 'management', 'securelab', 'lab']lab
        What kind of object is the Source Address?
         ('AnyIPAddress', 'IPv4Address', 'IPv4Network', 'IPv4Range',
         'objectRef#NetworkObj', 'objectRef#NetworkObjGroup')IPv4Address
        What is the source? 10.1.1.56
        What kind of object is the Destination Address?
         ('AnyIPAddress', 'IPv4Address', 'IPv4Network', 'IPv4Range',
         'objectRef#NetworkObj', 'objectRef#NetworkObjGroup')IPv4Network
        What is the destination? 10.2.2.0/24
        What kind of service needs to be opened?
         ('AnyService', 'ICMPService', 'NetworkProtocol', 'NetworkServiceGroups',
         'NetworkServiceObjects', 'TcpUdpService')TcpUdpService
        What service needs to be opened? tcp/22
        Please provide the Request #: 78910

        POST ACL CONFIG STATUS_CODE: 201 OK

    '''
    asa = input('What ASA would you like to modify? ')
    login_cred = ASAAAA(asa)
    header = login_cred.asa_login()

    intfc = input("What interface's policy would you like to modify?\n {} ".format(
        used_intfcs_name(asa, header)))
    position = get_acl_last_position(asa, header, intfc)

    config = config_variables(intfc, position)
    acl = ASAACL(asa, header)

    config_acl = acl.asa_configure_acl_access_in(intfc, config["source_kind"], config['source'],
                                                 config['destination_kind'], config['destination'],
                                                 config['service_kind'], config['service'], config['remark'],
                                                 config['position'])

    if config_acl.ok:
        print("\nPOST ACL CONFIG STATUS_CODE: {} OK\n".format(config_acl.status_code))
    else:
        print("\nPOST ACL CONFIG FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            config_acl.status_code, config_acl.reason, config_acl.content))


def config_variables(intfc, position):
    '''
    This function gets user's response to build the policy configuration,
    and formats it into a dictionary with values corresponding to the
    required variables of ASAACL.asa_configure_acl_access_in.

    Args:
        intfc: The interface corresponding to the policy being modified.
        position: The position which the new entry should be added to.

    Returns a dictionary of values that correspond with the required
    variables of ASAACL.asa_configure_acl_access_in. These will be
    used to apply the new policy to the Cisco ASA.

    '''
    network = ('AnyIPAddress', 'IPv4Address', 'IPv4Network', 'IPv4Range', 'objectRef#NetworkObj',
               'objectRef#NetworkObjGroup')
    service = ('AnyService', 'ICMPService', 'NetworkProtocol',
               'NetworkServiceGroups', 'NetworkServiceObjects', 'TcpUdpService')

    return {
        "interface_name": intfc,
        "source_kind": input('What kind of object is the Source Address? \n {} '.format(network)),
        "source": input('What is the source? '),
        "destination_kind": input('What kind of object is the Destination Address? \n {} '.format(network)),
        "destination": input('What is the destination? '),
        "service_kind": input('What kind of service needs to be opened? \n {} '.format(service)),
        "service": input('What service needs to be opened? '),
        "remark": input('Please provide the Request #: '),
        "position": position
    }


if __name__ == '__main__':
    main()
