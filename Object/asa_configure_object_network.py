import json
from asa_aaa_class import ASAAAA
from asa_object_class import ASAObject
from asa_routing_class import ASARouting
from asa_object_functions import determine_obj_key
from asa_routing_functions import sort_routes, route_used


def main():
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
    return {
        'host': input("What is the value of the new object? EX: 192.168.1.0/24# "),
        'desc': input("Please provide the host or network name# ")
    }


def make_name(kind, route, net):
    if kind == 'IPv4Address':
        prefix = '-host-'
    elif kind == 'IPv4Network':
        prefix = '-network-'
    else:
        prefix = '-range-'
    net = net.split('/')

    return route.zone + prefix + net[0] + '_' + net[1]


if __name__ == '__main__':
    main()
