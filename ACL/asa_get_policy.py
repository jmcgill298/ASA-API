import json
from asa_aaa_class import ASAAAA
from asa_acl_class import ASAACL
from asa_acl_functions import sort_acl
from asa_interface_functions import collected_interfaces


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
