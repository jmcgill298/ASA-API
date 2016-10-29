import json
from asa_aaa_class import ASAAAA
from asa_acl_class import ASAACL
from asa_acl_functions import sort_access_groups


def main():
    '''
    The purpose of this program is to list out the inbound ACLs and their
    corresponding interfaces. The ASAAAA class is used to establish a session,
    and the ASAACL class is used to collect the ACL configuration. The other
    functions are used to handle formatting. This is similar to a 'show run
    access-group' from the CLI of a Cisco ASA.

    Print:
        The mapping of all inbound ACLs and their corresponding interface

    Example:

        (py3) C:\\asa_api_tests>python asa_get_acls.py
        What ASA do you want to view? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input

        LOGIN STATUS_CODE: 204 OK

        ACL: lab_access_in
          Direction: IN
          Interface: lab
        ACL: weblab_access_in
          Direction: IN
          Interface: weblab

        '''
    login_cred = ASAAAA(asa=input('What ASA do you want to view? '))
    header = login_cred.asa_login()

    acls = ASAACL(login_cred.asa, header=header)
    access_groups = acls.asa_get_acls_in()

    if access_groups.ok:
        access_groups_json = json.loads(access_groups.text)
        print_access_groups(access_groups_json['items'])
    else:
        print("GET ACCESS GROUPS FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            access_groups.status_code, access_groups.reason, access_groups.content))


def print_access_groups(acls):
    '''
    This function is to print out the ACL configurations.

    Args:
         acls: A list of ACL configurations

    Print:
        The ACL, direction to apply policy, and the interface it is applied to.

    '''
    for acl in acls:
        acl = sort_access_groups(acl)
        print('ACL: {} \n  Direction: {} \n  Interface: {}'.format(
            acl['acl'], acl['direction'], acl['interface']))


if __name__ == '__main__':
    main()
