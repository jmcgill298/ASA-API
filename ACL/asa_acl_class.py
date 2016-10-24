import json
import requests
from asa_aaa_class import ASAAAA


def determiner(kind):
    '''
    The ASA API has two 'keys' used to refer to source, destination, and service values:
    Objects and Object Groups have a key of 'objectId,' all others have a key of 'value.'
    This function takes the source, destination, or service type, and returns the appropriate
    key. Since all 'values' with a 'key' of 'objectId' begin with 'objectRef', I use this as
    a test to return the appropriate key.

    Args:
        kind:  This is the kind of source, destination, or service being configured.
        Values are:
            AnyIPAddress = value
            IPv4Address = value
            IPv4Network = value
            IPv4Range = value
            objectRef#NetworkObj = objectId
            objectRef#Network = object Id

            AnyService = value
            ICMPService = value
            NetworkProtocol = value
            NetworkServiceGroups = objectId
            NetworkServiceObjects = objectId
            TcpUdpService = value

    Returns:
        The appropriate dictionary 'key' based on the kind of source, destination, or service.

    '''
    if "objectRef" in kind:
        return "objectId"
    else:
        return "value"


class ASAACL:
    '''Methods for making ACL related API calls to a Cisco ASA.

    The module initializes asa, base_url, and header used for all methods contained within.
    The methods are for interacting with Cisco ASAs using API calls instead of traditional
    CLI or ASDM. The methods will GET ACL related configurations, or make configuration
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
            What firewall would you like to use? 10.10.10.6
            >>>asa_login = ASAAAA(asa)
            What is your username? username
            Enter your password: getpass is used to hide password input
            >>>header = asa_login.asa_login()

            LOGIN STATUS_CODE: 204 OK

            >>>asa_acl = ASAACL(asa, header)

        '''
        self.asa = asa

        if header == None:
            self.header = ASAAAA().asa_login()
        else:
            self.header = header

        if base_url == None:
            self.base_url = "https://{}/api/access/".format(asa)
        else:
            self.base_url = base_url

    def asa_get_acls_in(self):
        '''
        This method returns the mapping between inbound ACLs and their corresponding interfaces.
        This is similar to the CLI 'show run access-group.'

        Returns:
            The request.get results for inbound ACLs configured on the given ASA.
            All desired printing should be handled by a program handling UI input/output.

        Example:

            >>>asa_acls = ASAACL(asa, header)
            >>>access_groups = asa_acls.asa_get_acls_in()
            >>>access_groups_json = json.loads(access_groups.text)
            >>>pprint(access_groups_json['items'])
            [{'ACLName': 'lab_access_in',
            'direction': 'IN',
            'interface': {'kind': 'objectRef#Interface',
                'name': 'lab',
                'objectId': 'GigabitEthernet0_API_SLASH_0',
                'refLink': 'https://10.10.10.5/api/interfaces/physical/
                GigabitEthernet0_API_SLASH_0'},
            'kind': 'object#AccessGroup',
            'selfLink': 'https://10.10.10.5/api/access/in/lab'},
            {'ACLName': 'weblab_access_in',
            'direction': 'IN',
            'interface': {'kind': 'objectRef#Interface',
               'name': 'weblab',
               'objectId': 'GigabitEthernet0_API_SLASH_2',
               'refLink': 'https://10.10.10.5/api/interfaces/physical/
               GigabitEthernet0_API_SLASH_2'},
            'kind': 'object#AccessGroup',
            'selfLink': 'https://10.10.10.5/api/access/in/weblab'}]

        '''
        url = self.base_url + 'in'
        return requests.get(url, verify=False, headers=self.header)

    def asa_get_acl_access_in(self, intfc_name):
        '''
        This method returns the inbound ACL policy for a given interface.
        This is similar to the CLI 'show access-list intfc_name.'

        Args:
            intfc_name: The name ('name-if') of the interface to use to display inbound ACL.

        Returns:
            The request.get results for inbound ACL policy entries used by the given interface.
            All desired printing should be handled by a program handling UI input/output.

        Example:

            >>>asa_acl = ASAACL(asa, header)
            >>>acl_policy = asa_acl.asa_get_acl_access_in('lab')
            >>>acl_policy_json = json.loads(acl_policy.text)
            >>>pprint(acl_policy_json['items'])
            [{'active': False,
            'destinationAddress': {'kind': 'AnyIPAddress', 'value': 'any4'},
            'destinationService': {'kind': 'NetworkProtocol', 'value': 'ip'},
            'isAccessRule': True,
            'kind': 'object#ExtendedACE',
            'objectId': '1559360646',
            'permit': True,
            'position': 1,
            'remarks': [Rule has been disabled],
            'ruleLogging': {'logInterval': 300, 'logStatus': 'Disabled'},
            'selfLink': 'https://10.10.10.5/api/access/in/lab/rules/1559360646',
            'sourceAddress': {'kind': 'objectRef#NetworkObj',
                'objectId': 'partner-network',
                'refLink': 'https://10.10.10.5/api/objects/networkobjects/partner-network'},
            'sourceService': {'kind': 'NetworkProtocol', 'value': 'ip'}},
            {'active': True,
            'destinationAddress': {'kind': 'AnyIPAddress', 'value': 'any4'},
            'destinationService': {'kind': 'NetworkProtocol', 'value': 'ip'},
            'isAccessRule': True,
            'kind': 'object#ExtendedACE',
            'objectId': '3535378664',
            'permit': True,
            'position': 2,
            'remarks': ['Approved ticket #1234'],
            'ruleLogging': {'logInterval': 300, 'logStatus': 'Informational'},
            'selfLink': 'https://10.10.10.5/api/access/in/lab/rules/3535378664',
            'sourceAddress': {'kind': 'IPv4Address', 'value': '10.1.1.2'},
            'sourceService': {'kind': 'NetworkProtocol', 'value': 'ip'}},
            {'active': True,
            'destinationAddress': {'kind': 'IPv4Address', 'value': '10.2.2.2'},
            'destinationService': {'kind': 'TcpUdpService', 'value': 'udp/syslog'},
            'isAccessRule': True,
            'kind': 'object#ExtendedACE',
            'objectId': '1172792386',
            'permit': True,
            'position': 13,
            'remarks': [],
            'ruleLogging': {'logInterval': 300, 'logStatus': 'Default'},
            'selfLink': 'https://10.10.10.5/api/access/in/lab/rules/1172792386',
            'sourceAddress': {'kind': 'IPv4Address', 'value': '10.1.1.2'},

        '''
        url = self.base_url + 'in/{}/rules'.format(intfc_name)
        return requests.get(url, verify=False, headers=self.header)

    def asa_configure_acl_access_in(self, intfc_name, src_kind, src, dst_kind, dst, svc_kind, svc, remark, position):
        '''
        This method uses the POST method to apply a new policy element to an existing inbound ACL.
        Since the ASA API varies on some 'key' values, the determiner function will be used to
        use the appropriate 'key.' There are many more parameters that can be used, however
        I only need these parameters, and do not want to add unnecessary complications.

        Args:
            intfc_name: The name of the interface which has the inbound ACL applied.
            src_kind: The type of source being configured (IP based or object based).
            src: The source to use in the ACL policy.
            dst_kind: The type of destination being configured (IP based or object based).
            dst: The source to use in the ACL policy.
            svc_kind: The type of destination service being configured (Protocol based or object based).
            svc: The destination service to use in the ACL policy.
            remark: A remark explaining the rules purpose.
            position: The position the new rule should occupy within the ACL

        Returns:
            A 'request.post()' which sends the configuration. All desired http return data should
            be handled by the UI function.

        Example:

            >>>asa_acl = ASAACL(asa, header)
            >>>acl_config = asa_acl.asa_configure_acl_access_in('lab', 'IPAddress', '10.1.4.28',
            'objectRef#NetworkObj','webhost', 'TcpUdpService', 'tcp/80', 'Approved Ticket: 5678', '20')
            >>>print('STATUS_CODE: {}'.format(acl_config.status_code))
            STATUS_CODE: 201

        '''
        url = self.base_url + 'in/{}/rules'.format(intfc_name)
        policy_config = {
            "sourceAddress": {
                "kind": src_kind,
                "{}".format(determiner(src_kind)): src
            },
            "destinationAddress": {
                "kind": dst_kind,
                "{}".format(determiner(dst_kind)): dst
            },
            "destinationService": {
                "kind": svc_kind,
                "{}".format(determiner(svc_kind)): svc
            },
            "ruleLogging": {
                "logInterval": "300",
                "logStatus": "Informational"
            },
            "permit": "true",
            "remarks": [remark],
            "position": position
        }

        return requests.post(url, verify=False, headers=self.header, json=policy_config)
