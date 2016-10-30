import json
from asa_aaa_class import ASAAAA
from asa_object_class import ASAObject


def main():
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
