import json
from asa_routing_functions import route_used


def determine_obj_key(obj):
    '''
    The ASA API has different 'values' used to refer to the kind of object being referenced:
    This function takes the object being created, and returns the appropriate 'value'.

    Args:
        obj: The object being created. The type of 'value' is determined by the object.
        Values are:
            0.0.0.0/0 = AnyIPAddress
            x.x.x.x = IPv4Address
            x.x.x.x/(0 < y < 32) = IPv4Network
            x.x.x.x-y.y.y.y = IPv4Range
            object network = objectRef#NetworkObj
            object-group network = objectRef#NetworkObjGroup

    Returns:
        The appropriate dictionary 'value' based on the kind of object.

    '''
    if obj == 'any4':
        return "AnyIPAddress"
    elif '/' in obj:
        return "IPv4Network"
    elif '-' in obj:
        return "Ipv4Range"
    elif 'NetworkObjGroup' in obj:
        return "objectRef#NetworkObjGroup"
    elif 'NetworkObj' in obj:
        return "objectRef#NetworkObj"
    else:
        return "IPv4Address"


def make_name(kind, route, net):
    '''
    This function is used to make the name of a new object based
    off the value of the object and standard naming conventions.

    Args:
        kind: The kind of object being created
        route: The routing entry the firewall would use to forward
        traffic for the given object.
        net: The value of the network object being configured

    Returns:
        The name of the new object using standard naming convention.
    '''
    if kind == 'IPv4Address':
        prefix = '-host-'
    elif kind == 'IPv4Network':
        prefix = '-network-'
    else:
        prefix = '-range-'

    net = net.split('/')

    return route.zone + prefix + net[0] + '_' + net[1]


def get_object_ip(obj_inst, object):
    '''
    This function takes a given ASAObject instance and a network object
    name and returns the IP value of the network.

    Args:
        obj_inst: An ASAObject
        object: The name of a configured object

    Returns:
        The IP value associated with the object.

    '''
    net_obj = obj_inst.asa_get_network_object(object)
    net_obj_json = json.loads(net_obj.text)

    return net_obj_json['host']['value']


def object_group_intfc(obj_inst, obj_grp, routes):
    '''
    This function takes a given ASAObject instance, object group ID,
    and routes from 'sort_routes' function and returns the interface
    which the object group's objects are reachable from.

    Args:
        obj_inst: An ASAObject
        obj_grp: The name of a configured object-group
        routes: A list of routes from the sort_routes function

    Returns:
        The name of the interface which would be used to forward traffic
        to the objects withing the object group.

    '''
    grp = obj_inst.asa_get_network_object_group(obj_grp).text
    grp_json = json.loads(grp)

    if 'objectRef#' in grp_json['members'][0]['kind']:
        ex_obj = grp_json['members'][0]['objectId']
        ex = get_object_ip(obj_inst, ex_obj)
    else:
        ex = grp_json['members'][0]['value']

    return route_used(routes, ex).zone
