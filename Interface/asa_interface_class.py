import json
import requests
from pprint import pprint
from asa_aaa_class import ASAAAA


class ASAInterface:
    '''
    Methods for making Interface related API calls to a Cisco ASA.

    The module initializes asa, header, and base_url used for all methods contained within.
    The methods are for interacting with Cisco ASAs using API calls instead of traditional
    CLI or ASDM. The methods will GET Interface related configurations, or make configuration
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

            >>>asa_interface = ASAAInterface(asa, header)

        '''
        self.asa = asa

        if header == None:
            self.header = ASAAAA().asa_login()
        else:
            self.header = header

        if base_url == None:
            self.base_url = "https://{}/api/interfaces/".format(asa)
        else:
            self.base_url = base_url

    def asa_get_phys_interface(self, hardware_id):
        '''
        This method is used to obtain the configuration for a single interface
        for a given ASA. This is similar to a 'show run interface x/y' on the CLI.

        Args:
            hardware_id: The interface of interest.

        Returns:
            The request.get results for a particular interface's configuration
            on the given ASA. All desired printing should be done by a program
            handling UI input/output.

        Example:

            >>>asa_intfc = ASAInterface(asa, header)
            >>>intfc_config = asa_intfc.asa_get_phys_interface(input('What interface would you like to view? '))
            What interface would you like to view? lab
            >>>intfc_config_json = json.loads(intfc_config.text)
            >>>pprint(intfc_config_json)
            {'activeMacAddress': '',
            'channelGroupID': '',
            'channelGroupMode': 'active',
            'duplex': 'auto',
            'flowcontrolHigh': -1,
            'flowcontrolLow': -1,
            'flowcontrolOn': False,
            'flowcontrolPeriod': -1,
            'forwardTrafficCX': False,
            'forwardTrafficSFR': False,
            'hardwareID': 'GigabitEthernet0/0',
            'interfaceDesc': 'to lab 5K',
            'ipAddress': {'ip': {'kind': 'IPv4Address', 'value': '192.168.1.14'},
                'kind': 'StaticIP',
                'netMask': {'kind': 'IPv4NetMask', 'value': '255.255.255.248'}},
            'ipv6Info': {'autoConfig': False,
                'dadAttempts': 1,
                'enabled': False,
                'enforceEUI64': False,
                'ipv6Addresses': [],
                'kind': 'object#Ipv6InterfaceInfo',
                'managedAddressConfig': False,
                'nDiscoveryPrefixList': [],
                'nsInterval': 1000,
                'otherStatefulConfig': False,
                'reachableTime': 0,
                'routerAdvertInterval': 200,
                'routerAdvertIntervalUnit': 'sec',
                'routerAdvertLifetime': 1800,
                'suppressRouterAdvert': False},
            'kind': 'object#GigabitInterface',
            'lacpPriority': -1,
            'managementOnly': False,
            'mtu': 1500,
            'name': 'lab',
            'objectId': 'GigabitEthernet0_API_SLASH_0',
            'securityLevel': 20,
            'selfLink': 'https://10.10.10.5/api/interfaces/physical/GigabitEthernet0_API_SLASH_0',
            'shutdown': False,
            'speed': 'auto',
            'standByMacAddress': ''}

        '''
        interface = hardware_id.split('/')
        url = self.base_url + 'physical/{}_API_SLASH_{}'.format(interface[0], interface[1])
        return requests.get(url, verify=False, headers=self.header)

    def asa_get_phys_interfaces(self):
        '''
        This method is used to obtain the configuration for a all interface
        for a given ASA. This is similar to a 'show run interface' on the CLI.

        Returns:
            The request.get results for the configuration of all interfaces
            on the given ASA. All desired printing should be done by a program
            handling UI input/output.

        Example:

            >>>asa_intfcs = ASAInterface(asa, header)
            >>>intfcs_config = asa_intfcs.asa_get_phys_interfaces()
            >>>intfc_config_json = json.loads(intfc_config.text)
            >>>pprint(intfc_config_json['text'])
            {'activeMacAddress': '',
             'channelGroupID': '',
             'channelGroupMode': 'active',
             'duplex': 'auto',
             'flowcontrolHigh': -1,
             'flowcontrolLow': -1,
             'flowcontrolOn': False,
             'flowcontrolPeriod': -1,
             'forwardTrafficCX': False,
             'forwardTrafficSFR': False,
             'hardwareID': 'GigabitEthernet0/0',
             'interfaceDesc': 'to lab 5K',
             'ipAddress': {'ip': {'kind': 'IPv4Address', 'value': '192.168.1.14'},
                         'kind': 'StaticIP',
                         'netMask': {'kind': 'IPv4NetMask', 'value': '255.255.255.248'}},
             'ipv6Info': {'autoConfig': False,
                         'dadAttempts': 1,
                         'enabled': False,
                         'enforceEUI64': False,
                         'ipv6Addresses': [],
                         'kind': 'object#Ipv6InterfaceInfo',
                         'managedAddressConfig': False,
                         'nDiscoveryPrefixList': [],
                         'nsInterval': 1000,
                         'otherStatefulConfig': False,
                         'reachableTime': 0,
                         'routerAdvertInterval': 200,
                         'routerAdvertIntervalUnit': 'sec',
                         'routerAdvertLifetime': 1800,
                         'suppressRouterAdvert': False},
             'kind': 'object#GigabitInterface',
             'lacpPriority': -1,
             'managementOnly': False,
             'mtu': 1500,
             'name': 'lab',
             'objectId': 'GigabitEthernet0_API_SLASH_0',
             'securityLevel': 20,
             'selfLink': 'https://10.10.10.5/api/interfaces/physical/GigabitEthernet0_API_SLASH_0',
             'shutdown': False,
             'speed': 'auto',
             'standByMacAddress': ''}
            {'activeMacAddress': '',
             'channelGroupID': '',
             'channelGroupMode': 'active',
             'duplex': 'auto',
             'flowcontrolHigh': -1,
             'flowcontrolLow': -1,
             'flowcontrolOn': False,
             'flowcontrolPeriod': -1,
             'forwardTrafficCX': False,
             'forwardTrafficSFR': False,
             'hardwareID': 'GigabitEthernet0/3',
             'interfaceDesc': '',
             'ipAddress': 'NoneSelected',
             'ipv6Info': {'autoConfig': False,
                         'dadAttempts': 1,
                         'enabled': False,
                         'enforceEUI64': False,
                         'ipv6Addresses': [],
                         'kind': 'object#Ipv6InterfaceInfo',
                         'managedAddressConfig': False,
                         'nDiscoveryPrefixList': [],
                         'nsInterval': 1000,
                         'otherStatefulConfig': False,
                         'reachableTime': 0,
                         'routerAdvertInterval': 200,
                         'routerAdvertIntervalUnit': 'sec',
                         'routerAdvertLifetime': 1800,
                         'suppressRouterAdvert': False},
             'kind': 'object#GigabitInterface',
             'lacpPriority': -1,
             'managementOnly': False,
             'mtu': 1500,
             'name': '',
             'objectId': 'GigabitEthernet0_API_SLASH_3',
             'securityLevel': -1,
             'selfLink': 'https://10.10.10.5/api/interfaces/physical/GigabitEthernet0_API_SLASH_3',
             'shutdown': True,
             'speed': 'auto',
             'standByMacAddress': ''}

        '''
        url = self.base_url + 'physical'
        return requests.get(url, verify=False, headers=self.header)

    def asa_config_phys_interface(self, hardware_id, security_level, name, ip_address, net_mask, description,
                                  mtu=1500, duplex='auto', speed='auto', shutdown='false', mgmt_only='false'):
        '''

        :param hardware_id:
        :param security_level:
        :param name:
        :param ip_address:
        :param net_mask:
        :param description:
        :param mtu:
        :param duplex:
        :param speed:
        :param shutdown:
        :param mgmt_only:
        :return:
        '''
        intfc = hardware_id.split('/')
        intfc_status = ASAInterface.asa_get_phys_interface(self=self, hardware_id=hardware_id).text
        intfc_status_json = json.loads(intfc_status)
        if intfc_status_json['shutdown']:
            kind = intfc_status_json["kind"]

            interface_config = {
                'securityLevel': security_level,
                'kind': kind,
                'channelGroupMode': 'active',
                'flowcontrolLow': -1,
                'name': name,
                'duplex': duplex,
                'hardwareID': hardware_id,
                'mtu': mtu,
                'lacpPriority': -1,
                'flowcontrolHigh': -1,
                'ipAddress': {
                    'ip': {
                        'kind': 'IPv4Address',
                        'value': ip_address
                    },
                    'kind': 'StaticIP',
                    'netMask': {
                        'kind': 'IPv4NetMask',
                        'value': net_mask
                    }
                },
                'flowcontrolOn': 'false',
                'shutdown': shutdown,
                'interfaceDesc': description,
                'managementOnly': mgmt_only,
                'channelGroupID': "",
                'speed': speed,
                'flowcontrolPeriod': -1,
                'forwardTrafficSFR': 'false',
                'forwardTrafficCX': 'false'
            }

            url = self.base_url + 'physical/{}_API_SLASH_{}'.format(intfc[0], intfc[1])
            return requests.put(url, verify=False, headers=self.header, json=interface_config)

        else:
            print("Interface currently in use! ")
            exit()
