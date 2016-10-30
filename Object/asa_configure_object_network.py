from asa_aaa_class import ASAAAA
from asa_object_class import ASAObject


def main():
    asa = input('What ASA do you want to configure? ')
    login_cred = ASAAAA(asa)
    header = login_cred.asa_login()

    config = config_variables()
    if '/32' in config['host']:
        config['host'] = config['host'].split('/')[0]

    net_obj = ASAObject(asa, header)
    config_obj = net_obj.asa_create_network_object(config['name'], config['host'], config['desc'])

    if config_obj.ok:
        print("\nPOST OBJECT CONFIG STATUS_CODE: {} OK\n".format(config_obj.status_code))
    else:
        print("\nPOST OBJECT CONFIG FAILED!!! STATUS_CODE: {}\nReason: {}\nContent: {}".format(
            config_obj.status_code, config_obj.reason, config_obj.content))


def config_variables():
    return {
        'name': input("What is the name of this object?# "),
        'host': input("What is the value of the new object? EX: 192.168.1.0/24# "),
        'desc': input("Please provide the host or network name# ")
    }


if __name__ == '__main__':
    main()
