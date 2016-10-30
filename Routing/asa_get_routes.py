import re
import json
from asa_aaa_class import ASAAAA
from asa_routing_class import ASARouting


def main():
    '''
    The purpose of this program is to list out the configured static routes.
    The ASAAAA class is used to establish a session, and the ASARouting class
    is used to collect the Routing configuration. The other functions are used
    to handle formatting. This is similar to a 'show run route' from the CLI
    of a Cisco ASA.

    Print:
        The static routes configured on the given ASA.

    Example:

        (py3) C:\\asa_api_tests>python asa_get_routes.py
        What ASA do you want to view? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input

        LOGIN STATUS_CODE: 204 OK

        Network 192.168.20.0/23 is reachable via 192.168.1.9 over interface
        GigabitEthernet0/0 in zone lab

        Network any4 is reachable via 10.1.1.1 over interface Management0/0
        in zone management

        Network 192.168.6.0/23 is reachable via 192.168.1.9 over interface
        GigabitEthernet0/0 in zone lab

        Network 192.168.12.0/23 is reachable via 192.168.1.17 over interface
        GigabitEthernet0/2 in zone weblab

    '''
    login_cred = ASAAAA(asa=input('What ASA do you want to view? '))
    header = login_cred.asa_login()

    routes = ASARouting(login_cred.asa, header=header)
    configured_routes = routes.asa_get_all_static_routes()

    if configured_routes.ok:
        configured_routes_json = json.loads(configured_routes.text)
        print_routes(configured_routes_json['items'])
    else:
        print("GET STATIC ROUTES FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            configured_routes.status_code, configured_routes.reason, configured_routes.content))

def print_routes(routes):
    '''
    This function collects the relevant information, formats the routing
    information, and then prints the data.


    Args:
        routes: a list of configured static routes

    Print:
        The routed network, gateway to reach the network, interface to
        reach this network, and what zone this network is in.

    '''
    for route in routes:
        (network, gateway, interface, zone) = (
            route['network']['value'],route['gateway']['value'],
            re.match('(?P<type>.*[0-9]).*(?P<int>[0-9]+)',route['interface']['objectId']),
            route['interface']['name']
        )
        print('Network {} is reachable via {} over interface {}/{} in zone {}\n'.format(
            network, gateway, interface.group('type'), interface.group('int'), zone))

if __name__ == '__main__':
    main()
    
