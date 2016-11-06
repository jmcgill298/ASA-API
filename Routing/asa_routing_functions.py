import re
from netaddr import IPNetwork
from collections import namedtuple

def sort_routes(routes):
    '''
    This function takes the json formatted route data, and returns a
    list of named tuples for Network to route, Gateway to reach the
    network, Interface to use, and zone this network is in.

    Args:
        routes: A list of json formatted routes from an ASA API call.

    Returns:
         A list of named tuples with only relevant fields extracted.

    '''
    static_routes = []
    for route in routes:
        hw_id = re.match('(?P<type>.*[0-9]).*(?P<int>[0-9]+)', route['interface']['objectId'])
        net_route = namedtuple('net_route', 'network gateway intfc zone')
        static_route = net_route(
            route['network']['value'],
            route['gateway']['value'],
            hw_id.group('type') + '/' + hw_id.group('int'),
            route['interface']['name']
        )
        static_routes.append(static_route)
    return static_routes


def route_used(routes, net):
    '''
    This function takes a list of routes from sort_routes, and
    returns the specific route an ASA should use for a given network.
    The management interface is removed from consideration.

    Args:
        routes: A list of routes from an ASA formatted from sort_routes.
        network: A network that needs to be routed on an ASA.

    Returns:
        The routing information for the given network.

    '''
    possible_routes = []
    for route in routes:
        if 'Management' in route.intfc:
            pass
        elif route.network == 'any4':
            value = '0.0.0.0/0'
        else:
            value = route.network
        if IPNetwork(net) not in IPNetwork(value):
            pass
        elif len(possible_routes) == 0 or possible_routes[-1].network == 'any4':
            possible_routes.append(route)
        else:
            if IPNetwork(possible_routes[-1]) < IPNetwork(value):
                possible_routes.append(route)

    return possible_routes[-1]
