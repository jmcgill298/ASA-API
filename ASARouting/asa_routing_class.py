import json
import requests


class ASARouting:
    '''Methods for making Routing related API calls to a Cisco ASA.

    The module initializes asa, base_url, and header used for all methods contained within.
    The methods are for interacting with Cisco ASAs using API calls instead of traditional
    CLI or ASDM. The methods will GET Routing related configurations, or make configuration
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

            >>>asa_acl = ASAARouting(asa, header)

        '''
        self.asa = asa

        if header == None:
            self.header = ASAAAA().asa_login()
        else: self.header = header

        if base_url == None:
            self.base_url = "https://{}/api/routing/".format(asa)
        else: self.base_url = base_url


    def asa_get_all_static_routes(self):
        '''
        This method is used to obtain a list of static routes configured on the
        given ASA formatted in json. This is similar to a 'show run route' on the CLI.

        Returns:
            The request.get results for Routes configured on the given ASA.
            All desired printing should be done by a program handling UI input/output.

        Example:
        
            >>>asa_routes = ASARouting(asa, header)
            >>>routes = asa_routes.asa_get_all_static_routes()
            >>>routes_json = json.loads(asa_routes.text)
            >>>pprint(routes_json['items'])
            [{'distanceMetric': 1,
            'gateway': {'kind': 'IPv4Address', 'value': '192.168.1.9'},
            'interface': {'kind': 'objectRef#Interface',
                'name': 'lab',
                'objectId': 'GigabitEthernet0_API_SLASH_0',
                'refLink': 'https://10.10.10.5/api/interfaces/physical/
                GigabitEthernet0_API_SLASH_0'},
            'kind': 'object#IPv4Route',
            'network': {'kind': 'IPv4Network', 'value': '192.168.2.20/23'},
            'objectId': '264df607',
            'selfLink': 'https://10.10.10.5/api/routing/static/264df607',
            'tracked': False,
            'tunneled': False},
            {'distanceMetric': 1,
            'gateway': {'kind': 'IPv4Address', 'value': '192.168.1.17'},
            'interface': {'kind': 'objectRef#Interface',
                'name': 'weblab',
                'objectId': 'GigabitEthernet0_API_SLASH_2',
                'refLink': 'https://10.10.10.5/api/interfaces/physical/
                GigabitEthernet0_API_SLASH_2'},
            'kind': 'object#IPv4Route',
            'network': {'kind': 'IPv4Network', 'value': '192.168.12.0/23'},
            'objectId': '2817b577',
            'selfLink': 'https://10.10.10.5/api/routing/static/2817b577',
            'tracked': False,
            'tunneled': False}]

        '''
        url = self.base_url + 'static'
        return requests.get(url, verify=False, headers=self.header)


    def asa_add_static_route(self, network, gateway, zone):
        '''
        This method is used to configure a new static route on a Cisco ASA.

        Args:
            network: The network which needs to be added to the routing table.
            gateway: The gateway through which this network can be reached.
            zone: The zone on the firewall this interface belongs to.

        Returns:
            A 'request.post()' which sends the configuration. All desired http return data
            should be handled by the UI function.

        '''
        url = self.base_url + 'static'
        route_config = {
            "tunneled": "false",
            "kind": "object#IPv4Route",
            "distanceMetric": 1,
            "tracked": "false",
            "interface": {
                "kind": "objectRef#Interface",
                "name": zone
            },
            "gateway": {
                "kind": "IPv4Address",
                "value": gateway
            },
            "network": {
                "kind": "IPv4Network",
                "value": network
            }
        }

        return requests.post(url, verify=False, headers=self.header, json=route_config)
