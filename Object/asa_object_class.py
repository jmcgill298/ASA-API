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

    def asa_get_network_object(self, object):
        '''
        This method returns a GET request for obtaining network object configurations.
        This is similar to a 'show run object network' on the CLI.

        Args:
            object: The name of the object to retrieve on the ASA.

        Returns:
            The request.get results for network objects configured on the given ASA.
            All desired printing should be handled by a program handling UI input/output.

        Example:

            >>>asa_object = ASAObject(asa, header)
            >>>net_object = asa_object.asa_get_network_objects()
            >>>net_object_json = json.loads(net_object.text)
            >>>pprint(net_object_json)
            {'description': 'LABDBWD0002',
             'host': {'kind': 'IPv4Address', 'value': '192.168.6.98'},
             'kind': 'object#NetworkObj',
             'name': 'lab-host-192.168.6.98_32',
             'objectId': 'lab-host-192.168.6.98_32',
             'selfLink': 'https://10.10.10.5/api/objects/networkobjects/lab-host-192.168.6.98_32'},

        '''
        url = self.base_url + 'objects/networkobjects/' + object
        net_object = requests.get(url, verify=False, headers=self.header)

        return net_object

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
            [{'description': 'LABDBWD0002',
              'host': {'kind': 'IPv4Address', 'value': '192.168.6.98'},
              'kind': 'object#NetworkObj',
              'name': 'lab-host-192.168.6.98_32',
              'objectId': 'lab-host-192.168.6.98_32',
              'selfLink': 'https://10.10.10.5/api/objects/networkobjects/lab-host-192.168.6.98_32'},
             {'description': 'Web Server Network',
              'host': {'kind': 'IPv4Network', 'value': '192.168.12.0/24'},
              'kind': 'object#NetworkObj',
              'name': 'web-network',
              'objectId': 'web-network',
              'selfLink': 'https://10.10.10.5/api/objects/networkobjects/web-network'},
             {'description': 'SSO Range',
              'host': {'kind': 'IPv4Range', 'value': '192.168.10.10-192.168.10.12'},
              'kind': 'object#NetworkObj',
              'name': 'sso-range',
              'objectId': 'sso-range',
              'selfLink': 'https://10.10.10.5/api/objects/networkobjects/sso-range'}]

        '''
        url = self.base_url + 'objects/networkobjects'
        net_objects = requests.get(url, verify=False, headers=self.header)

        return net_objects

    def asa_get_network_object_group(self, group):
        '''
        This method returns a GET request for obtaining a specific network
        object configured on an ASA. This is similar to a 'show run object-group
        id (object group name)' on the CLI.

        Args:
            group: The name of the object

        Returns:
            The request.get results for a particular network object group
            configured on the given ASA. All desired printing should be
            handled by a program handling UI input/output.

        Example:

            >>>asa_object = ASAObject(asa, header)
            >>>net_object_grp = asa_object.asa_get_network_object_group('grp-web-servers')
            >>>net_object_grp_json = json.loads(net_object_grp.text)
            >>>pprint(net_object_grp_json['items'])
            {'description': 'All Web Servers',
             'kind': 'object#NetworkObjGroup',
             'members': [{'kind': 'IPv4Address', 'value': '192.168.12.58'},
                         {'kind': 'objectRef#NetworkObj',
                          'objectId': 'webserver0001',
                          'refLink': 'https://10.10.10.5/api/objects/networkobjects/webserver0001'}],
             'name': 'grp-web-servers',
             'objectId': 'grp-web-servers',
             'selfLink': 'https://10.10.10.5/api/objects/networkobjectgroups/grp-web-servers'}

        '''
        url = self.base_url + 'objects/networkobjectgroups/' + group
        net_object_group = requests.get(url, verify=False, headers=self.header)

        return net_object_group

    def asa_get_network_object_groups(self):
        '''
        This method returns a GET request for obtaining network object groups configured
        on an ASA. This is similar to a 'show run object-group id (object)' on the CLI.

        Returns:
            The request.get results for network object groups configured on
            the given ASA. All desired printing should be handled by a program
            handling UI input/output.

        Example:
            >>>asa_object = ASAObject(asa, header)
            >>>net_object_grps = asa_object.asa_get_network_object_groups()
            >>>net_object_grps_json = json.loads(net_object_grps.text)
            >>>pprint(net_object_grps_json)
            [{'description': 'Website Database Servers',
              'kind': 'object#NetworkObjGroup',
              'members': [{'kind': 'IPv4Address', 'value': '192.168.10.40'},
                          {'kind': 'objectRef#NetworkObj',
                           'objectId': 'database0001',
                           'refLink': 'https://10.10.10.5/api/objects/networkobjects/database0001'}],
              'name': 'grp-databases',
              'objectId': 'grp-databases',
              'selfLink': 'https://10.10.10.5/api/objects/networkobjectgroups/grp-databases'},
             {'description': 'All Web Servers',
              'kind': 'object#NetworkObjGroup',
              'members': [{'kind': 'IPv4Address', 'value': '192.168.12.58'},
                          {'kind': 'objectRef#NetworkObj',
                           'objectId': 'webserver0001',
                           'refLink': 'https://10.10.10.5/api/objects/networkobjects/webserver0001'}],
              'name': 'grp-web-servers',
              'objectId': 'grp-web-servers',
              'selfLink': 'https://10.10.10.5/api/objects/networkobjectgroups/grp-web-servers'}]

        '''
        url = self.base_url + 'objects/networkobjectgroups'
        net_object_groups = requests.get(url, verify=False, headers=self.header)

        return net_object_groups

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
