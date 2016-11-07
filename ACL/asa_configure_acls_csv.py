import sys
import json
from csv import DictReader
from asa_aaa_class import ASAAAA
from asa_acl_class import ASAACL
from asa_object_class import ASAObject
from asa_routing_class import ASARouting
from asa_object_functions import object_group_intfc
from asa_acl_functions import get_acl_last_position
from asa_routing_functions import sort_routes


def main(csv):
    '''
    The purpose of this program is to configure new lines of policy to
    existing ACLs on a Cisco ASA. The ASAAAA class is used to establish a
    session, the ASAObject and ASARouting classes are used to help determine 
    which interface the source object group is associated with, and the ASAACL
    class is used to POST the new ACL configuration policy. The other functions
    are used to collect configuration and handle formatting. This is similar to
    an 'access-list acl_name remark remark' and 'access-list acl_name extended
    [permit,deny] source destination service log' from the CLI of a Cisco ASA.

    Print:
        The configuration result: A 201 means the configuration was applied,
        other codes indicate an issue with the request. Failures do print
        the code, reason, and content of the response.

    Example:
        (py3) C:\\asa_api_tests>python asa_configure_acls_csv.py asa_new_policy.csv
        What ASA would you like to modify? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input

        LOGIN STATUS_CODE: 204 OK

        POST ACL CONFIG STATUS_CODE: 201 OK

        POST ACL CONFIG STATUS_CODE: 201 OK

        CSV file reads:
            Source Application,Source,Destination Application,Destination,Protocol,
            Justification,Remark
            Network Engineering,grp-lab-neteng-networks,Thousand Eyes,grp-weblab-thousandeyes-monitors,
            grp-tcp-https,Network Engineering MGMT,RITM00029
            Thousand Eyes,grp-weblab-thousandeyes-monitors,Thousand Eyes,grp-securelab-thousandeyes-db,
            grp-tcpudp-thousandeyes,Thousand Eyes DB Access,RITM00029

    '''
    asa = input('What ASA would you like to modify? ')
    login_cred = ASAAAA(asa)
    header = login_cred.asa_login()

    obj = ASAObject(asa, header)
    acl = ASAACL(asa, header)
    routes = ASARouting(asa, header)

    config_acls(csv, asa, header, obj, acl, routes)


def config_acls(csv, asa, header, obj, acl, routes):
    '''
    This function is uses the 'asa_configure_acl_access_in' method
    to configure new ACL policies from a CSV file. csv.DictReader is
    used to provide names for common variables, and sort_routes is used
    to provide the routing table for the given ASA. The function then
    loops over each row in the CSV file and determines the appropriate
    ACL, position in the ACL, and applies the necessary configuration
    parameters to the necessary ACL on the given ASA. The CSV should use
    object groups for sources, destinations, and destination services.
    
    Args:
        csv: A CSV file containing necessary configuration info:
        source group, destination group, destination service and remark.
        asa: The ASA to apply the new policy.
        header: The header from an established ASAAAA object.
        obj: An ASAObject instance.
        acl: An ASAACL instance.
        routes: An ASARouting instance.
    
    Print:
        The configuration result: A 201 means the configuration was applied,
        other codes indicate an issue with the request. Failures do print
        the code, reason, and content of the response.
    
    '''
    acl_csv = DictReader(open(csv))
    sorted_routes = sort_routes(json.loads(routes.asa_get_all_static_routes().text)['items'])

    for policy in acl_csv:
        src, dst, svc, remark = policy['Source'], policy['Destination'], policy['Protocol'], policy['Remark']
        intfc = object_group_intfc(obj, src, sorted_routes)
        position = get_acl_last_position(asa, header, intfc)

        config_acl = acl.asa_configure_acl_access_in(intfc,
                                                     'objectRef#NetworkObjGroup', src,
                                                     'objectRef#NetworkObjGroup', dst,
                                                     'objectRef#NetworkServiceGroup', svc,
                                                     remark, position)

        if config_acl.ok:
            print("\nPOST ACL CONFIG STATUS_CODE: {} OK\n".format(config_acl.status_code))
        else:
            print("\nPOST ACL CONFIG FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
                config_acl.status_code, config_acl.reason, config_acl.content))


if __name__ == '__main__':
    main(sys.argv[1])
