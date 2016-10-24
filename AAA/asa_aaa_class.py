import json
import requests
from getpass import getpass


class ASAAAA:
    '''Methods for making AAA related API calls to a Cisco ASA.
    The module initializes asa, username, password and base_url used for all
    methods contained within. The methods are for interacting with Cisco ASAs
    using API calls instead of traditional CLI or ASDM. The methods will handle
    authentication related tasks, or make configuration changes using POST, PUT,
    and PATCH via the requests module.
    '''
    def __init__(self, asa, un=None, pw=None, base_url=None):
        '''
        The __init__ method requires an ASA name or IP that can be used to make API
        calls. The un and pw can be entered, but it is expected that they will be
        left blank, and will be handled by method prompts. The pw uses the getpass
        in order to keep the password from being echoed back to the screen. The
        base_url will also default to the correct base URL used for all of the
        methods within this class; each method will build on this base URL to build
        the full URL need to obtain the method's goal.
        Args:
            asa: The IP or hostname to be used to reach the desired ASA.
            un: The username for the user trying to login.
            pw: The password for the user trying to login.
            base_url: The base URL used by all API calls in the module.
        Example:
            >>>asa = input('What firewall would you like to use? ')
            >>>What firewall would you like to use? 10.10.10.5
            >>>asa_login = ASAAAA(asa)
            What is your username? username
            Enter your password: getpass is used to hide password input
            >>>header = asa_login.asa_login()
            LOGIN STATUS_CODE: 204 OK
        '''
        self.asa = asa

        if un == None:
            self.un = input('What is your username? ')
        else: self.un = un

        if pw == None:
            self.pw = getpass('Enter your password: ')
        else: self.pw = pw

        if base_url == None:
            self.base_url = "https://{}/api".format(asa)
        else: self.base_url = base_url


    def asa_login(self):
        '''
        This module is used to login to the given ASA and return
        a token to reuse for future requests.
        Returns:
             A header with 'Content-Type json and a 'X-Auth-Token.'
             
        '''
        requests.packages.urllib3.disable_warnings()

        url = self.base_url + "/tokenservices"
        body = json.dumps({})

        asa_session = requests.Session()
        asa_session.auth = (self.un, self.pw)
        login = asa_session.post(url,json=body,verify=False)
        if login.ok:
            print("\nLOGIN STATUS_CODE: {} OK \n".format(login.status_code))
            headers = login.headers
            headers['Content-Type'] = 'application/json'
            return headers
            
