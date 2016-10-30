import json
from asa_acl_class import ASAACL


def sort_access_groups(acl):
    '''
    This function pulls out the interesting fields and returns them in a dictionary.

    Args:
        acl: The configuration of a ACL

    Returns:
         Only the interesting values of the ACL as a dictionary.

    '''
    return {'acl': acl["ACLName"], 'direction': acl["direction"], 'interface': acl["interface"]["name"]}


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


def get_acl_last_position(asa, header, intfc_name):
    '''
    This function is used to get the position of the current last item
    in the ACL. The new ACL entry will use this same number to add
    the entry 1 position from the bottom; this is done to place above
    an explicit 'deny all.'

    Args:
        asa: The IP or hostname to be used to reach the desired ASA.
        header: The header to use for providing the authentication token.
        intfc_name: The name of the interface which is being modified.

    Returns:
         The number in string format of the current last item in the policy.

    '''
    acl = ASAACL(asa, header)
    acls = acl.asa_get_acl_access_in(intfc_name)
    acls_json = json.loads(acls.text)['items']
    return acls_json[-1]["position"]
