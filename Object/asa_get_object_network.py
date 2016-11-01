import json
from asa_aaa_class import ASAAAA
from asa_object_class import ASAObject


def main():
    '''
    The purpose of this program is to list out the configured network objects.
    The ASAAAA class is used to establish a session, and the ASAObject class
    is used to collect then network objects. The other functions are used to
    handle formatting. This is similar to a 'show run object network' from the
    CLI of a Cisco ASA.

    Print:
           The network objects configured on the given ASA.

    Example:

        (py3) C:\\asa_api_tests>python asa_get_object_network.py
        What ASA do you want to view? 10.10.10.5
        What is your username? username
        Enter your password: getpass is used to hide password input

        LOGIN STATUS_CODE: 204 OK

        GET NETWORK OBJECT STATUS_CODE: 200 OK

        lab-server-192.168.6.8_32
         lab server
         192.168.6.8

        weblab-range-192.168.12.7_20
         Weblab Range for HTTP Servers
         192.168.12.7-192.168.12.20

        securelab-network-192.168.11.44_32
         LABWSWP00023
         192.168.11.44

        weblab-network-192.168.12.64_26
         Weblab HTTPS Servers
         192.168.12.64/26

    '''
    asa = input('What ASA do you want to view? ')
    login_cred = ASAAAA(asa)
    header = login_cred.asa_login()

    asa_objects = ASAObject(asa, header)
    net_objects = asa_objects.asa_get_network_objects()

    if net_objects.ok:
        print("GET NETWORK OBJECT STATUS_CODE: {} OK \n".format(net_objects.status_code))
        net_objects_json = json.loads(net_objects.text)['items']
        print_net_objects(net_objects_json)
    else:
        print("GET NETWORK OBJECTS FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            net_objects.status_code, net_objects.reason, net_objects.content))

def print_net_objects(objects):
    '''
    This function is used to sort out the relevant network
    object information and print the network objects.

    Args:
        objects: The json formatted response of network objects
        from an ASA

    Prints:
        The network objects of the given ASA

    '''
    for object in objects:
        name = object["name"]
        value = object["host"]["value"]
        try:
            desc = object["description"]
        except:
            desc = 'None'

        print('\n{}\n {}\n {}'.format(name, desc, value))


if __name__ == '__main__':
    main()
