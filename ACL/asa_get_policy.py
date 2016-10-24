import json
from asa_aaa_class import ASAAAA
from asa_acl_class import ASAACL
from asa_interface_class import ASAInterface


def main():
    '''
    The purpose of this program is to list out the inbound ACL policy for a particular
    interface. The ASAAAA class is used to establish a session, the ASAInterface class
    is used to provide a list currently used interfaces, and the ASAACL class is used
    to collect the policy for the given interface. The other functions are used to handle
    formatting. This is similar to a 'show run access-list acl_name' from the CLI of a
    Cisco ASA.
    Print:
        The active policy entries for the particular interface is printed out in the format:
        (permit or deny) source (source) destination (destination) protocol (protocol[/port])
    Example:
        (py3) C:\\asa_api_tests>python asa_get_policy.py
        What ASA do you want to view? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input
        LOGIN STATUS_CODE: 204 OK
        What interface's would you like to view?
        ['weblab', 'management', 'securelab', 'lab'] lab
        permit source 10.1.1.22 destination any protocol ip
        permit source 10.1.1.53 destination 10.2.2.22 protocol udp
        permit source 10.1.1.28 destination 10.2.2.33 protocol icmp/echo
        permit source 10.1.1.28 destination 10.2.2.0/24 protocol web_protos
        permit source 10.1.1.29 destination web_servers protocol tcp/http
    '''
    login_cred = ASAAAA(asa=input('What ASA do you want to view? '))
    header = login_cred.asa_login()

    intfc = input("What interface's would you like to view?\n{} ".format(
        collected_interfaces(login_cred.asa, header)))
    print()
    acl = ASAACL(login_cred.asa, header)
    policy = acl.asa_get_acl_access_in(intfc)

    if policy.ok:
        policy_json = json.loads(policy.text)
        print_acls(policy_json['items'])
    else:
        print("GET POLICY FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: ".format(
            policy.status_code, policy.reason, policy.content))


def collected_interfaces(asa, header):
    '''This function uses ASAInterface class to collect the Interfaces,
    and returns just the names of used interfaces
    Args:
        asa: The IP or hostname to be used to reach the desired ASA.
        header: The header to use for providing the authentication token.
    Returns:
         A list of currently used interfaces
    '''
    intfc_config = ASAInterface(asa, header)
    intfcs = intfc_config.asa_get_phys_interfaces()
    used_intfcs = []
    for intfc in intfcs:
        if not intfc["shutdown"]:
            used_intfcs.append(intfc["name"])

    return used_intfcs


def sort_acl(acl):
    '''
    The ASA API for ACLs uses different 'keys' for same policy element depending
    if it is object based or not. This function is used to sort through each rule
    in the ACL and use the correct 'keys' to return the interesting values.
    Args:
        acl: A line entry in an ACL
    Returns:
        A dictionary of the interesting fields
    '''
    if acl['permit']:
        permission = 'permit'
    else:
        permission = 'deny'

    if acl['sourceAddress']['kind'] == 'AnyIPAddress':
        source = 'any'
    elif 'objectRef#' in acl['sourceAddress']['kind']:
        source = acl['sourceAddress']['objectId']
    else:
        source = acl['sourceAddress']['value']

    if acl['destinationAddress']['kind'] == 'AnyIPAddress':
        destination = 'any'
    elif 'objectRef' in acl['destinationAddress']['kind']:
        destination = acl['destinationAddress']['objectId']
    else:
        destination = acl['destinationAddress']['value']

    if 'objectRef' in acl['destinationService']['kind']:
        service = acl['destinationService']['objectId']
    else:
        service = acl['destinationService']['value']

    return {'permission': permission, 'source': source, 'destination': destination, 'service': service}


def print_acls(acls):
    '''
    This function takes an ACL, filters out the 'disabled' rules, then puts each line
    through sort_acl to return only the interesting values, and then prints the results.
    Args:
        acls: A list of an interface's ACL policy
    Prints:
        One line per 'active' entry to display the policies configuration.
    '''
    for entry in acls:
        if entry['active']:
            acl = sort_acl(entry)
            print('{} source {} destination {} protocol {}'.format(
                acl['permission'], acl['source'], acl['destination'], acl['service']))


if __name__ == '__main__':
    main()
