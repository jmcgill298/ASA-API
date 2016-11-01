import json
import requests
from asa_aaa_class import ASAAAA
from asa_object_functions import determine_obj_key


class ASAObject:
    '''Methods for making Object related API calls to a Cisco ASA.

    The module initializes asa, header, and base_url used for all methods contained within.
    The methods are for interacting with Cisco ASAs using API calls instead of traditional
    CLI or ASDM. The methods will GET Object related configurations, or make configuration
    changes using POST, PUT, and PATCH via the requests module.

    '''

    def __init__(self, asa, header=None, base_url=None):
        '''
        The __init__ method requires an ASA name or IP that can be used to make API calls.
        It is expected that the ASAAAA class will be used to obtain a header containing a
        valid authentication token; however, a user will be prompted to initialize ASAAAA and
        obtain the necessary token if none is provided. The default base URL is based on Cisco's
        API documentation; all methods will build off the base URL for making an API call.

        Args:
            asa: The IP or hostname to be used to reach the desired ASA.
            header: The header to use for providing the authentication token.
            base_url: The base URL used by all API calls in the module.

        Example:
            >>>asa = input('What firewall would you like to use? ')
            What firewall would you like to use? 10.10.10.5
            >>>asa_login = ASAAAA(asa)
            What is your username? username
            Enter your password: getpass is used to hide password input
            >>>header = asa_login.asa_login()

            LOGIN STATUS_CODE: 204 OK

            >>>asa_object = ASAObject(asa, header)

        '''
        self.asa = asa

        if header == None:
            self.header = ASAAAA(asa)
        else:
            self.header = header

        if base_url == None:
            self.base_url = "https://{}/api/".format(asa)
        else:
            self.base_url = base_url

    def asa_get_network_objects(self):
        '''
        This method returns a GET request for obtaining network object configurations.
        This is similar to a 'show run object network' on the CLI.

        Returns:
            The request.get results for network objects configured on the given ASA.
            All desired printing should be handled by a program handling UI input/output.

        Example:

            >>>asa_objects = ASAObject(asa, header)
            >>>net_objects = asa_objects.asa_get_network_objects()
            >>>net_objects_json = json.loads(net_objects.text)
            >>>pprint(net_objects_json['items'])

        '''
        url = self.base_url + 'objects/networkobjects'
        net_objects = requests.get(url, verify=False, headers=self.header)

        return net_objects

    def asa_create_network_object(self, name, obj, desc):
        '''
        This method returns a POST request for configuring a network object on the
        given ASA. This is similar to an 'object network name' from the CLI.

        Args:
            name: The name of the network object
            obj: The IP, Range, or Subnet the object represents.
            desc: A description of the object.

        Returns:
            The request.post results for creating the network object.

        Example:

            >>>asa_object = ASAObject(asa, header)
            >>>net_object_config = asa_object.asa_create_network_object(name, obj, desc)
            >>>print('STATUS_CODE: {}'.format(net_object_config.status_code))
            STATUS_CODE: 201

        '''
        url = self.base_url + 'objects/networkobjects'
        network_objects_config = {
            'name': name,
            'host': {
                'kind': '{}'.format(determine_obj_key(obj)),
                'value': obj
            },
            'description': desc,
            'kind': 'object#NetworkObj'
        }

        return requests.post(url, verify=False, headers=self.header, json=network_objects_config)
