import json
import requests
from asa_aaa_class import ASAAAA
from pprint import pprint


def determine_obj_key(obj):
    '''
    The ASA API has different 'values' used to refer to the kind of object being referenced:
    This function takes the object being created, and returns the appropriate 'value'.

    Args:
        obj: The object being created. The type of 'value' is determined by the object.
        Values are:
            0.0.0.0/0 = AnyIPAddress
            x.x.x.x/32 = IPv4Address
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