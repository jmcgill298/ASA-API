import json
from asa_aaa_class import ASAAAA
from asa_object_class import ASAObject
from asa_routing_class import ASARouting
from asa_routing_functions import sort_routes, route_used
from asa_object_functions import determine_obj_key, make_name


def main():
    '''
    The purpose of this program is to configure a new network object using
    standard naming conventions. The ASAAAA class is used to establish a session,
    the ASARouting class is used to collect the current routes, and the ASAObject
    class is used to configure the new network object. The other functions are
    used to handle formatting. This is similar to a 'object network name' from
    the CLI of a Cisco ASA.

    Print:
        The configuration result: A 201 means the configuration was applied,
        other codes indicate an issue with the request. Failures do print
        the code, reason, and content of the response.

    Example:

        (py3) C:\\asa_api_tests>python asa_configure_object_network.py
        What ASA do you want to view? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input

        LOGIN STATUS_CODE: 204 OK

        What is the value of the new object? EX: 192.168.1.0/24# 192.168.6.98/32
        Please provide the host or network name# LABDB002

        POST OBJECT CONFIG STATUS_CODE: 201 OK

        ASA CLI Config Results in:
        object network lab-network-192.168.6.98_32
         host 192.168.6.98
         description LABDB002

    '''
    asa = input('What ASA do you want to configure? ')
    login_cred = ASAAAA(asa)
    header = login_cred.asa_login()

    routes = ASARouting(asa, header)
    asa_routes = routes.asa_get_all_static_routes().text
    sorted_routes = sort_routes(json.loads(asa_routes)['items'])

    config = config_variables()
    used_route = route_used(sorted_routes, config['host'])
    key = determine_obj_key(config['host'])
    obj_name = make_name(key, used_route, config['host'])

    if '/32' in config['host']:
        config['host'] = config['host'].split('/')[0]

    net_obj = ASAObject(asa, header)
    config_obj = net_obj.asa_create_network_object(obj_name, config['host'], config['desc'])

    if config_obj.ok:
        print("\nPOST OBJECT CONFIG STATUS_CODE: {} OK\n".format(config_obj.status_code))
    else:
        print("\nPOST OBJECT CONFIG FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            config_obj.status_code, config_obj.reason, config_obj.content))


def config_variables():
    '''This function collects the configuration parameters.

    Returns:
        A dictionary used to assign host and description values
        for the new network object.

    '''
    return {
        'host': input("What is the value of the new object? EX: 192.168.1.0/24# "),
        'desc': input("Please provide the host or network name# ")
    }


if __name__ == '__main__':
    main()
