import re
from collections import namedtuple

def sort_routes(routes):
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
