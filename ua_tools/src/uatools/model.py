'''
CGI INTERNAL USE ONLY

model.py is part of uatools package and is a collection of classes allowing GET queries to UA Gateway devices and parse
specific collected data such as AAA current usage or VPN Vserver current usage

Author: Vincent Corriveau (vincent.corriveau@cgi.com)
'''
import requests, urllib3
from requests import Timeout

from uatools.logger import get_logger

LOGGER = get_logger('uatools.vpn_usage')
AUTH_HEADERS = {
    'X-NITRO-USER': 'nsroot',
    'X-NITRO-PASS': 'lan0wan0'  # Password can be found in Password Safe
}


class Parser:
    """A JSON reader for nitro API response"""
    def __init__(self, gateway_type: str):
        self.aaa_parse_strategy = getattr(self, f'_ua_{gateway_type.lower()}_aaa_parser',
                                          self._default_aaa_parser)
        self.vserver_parse_strategy = self._default_vsrv_parser

    def _ua_lite_aaa_parser(self, content: dict):
        return content['aaa']['aaacurtmsessions']

    def _default_aaa_parser(self, content: dict):
        return content['aaa']['aaacursessions']

    def _default_vsrv_parser(self, content: dict):
        res = dict()
        # vserver can only be parse if the content dict as a key named "vpnvserver"
        if 'vpnvserver' in content:
            for data in [running_vserver for running_vserver in content['vpnvserver'] if
                         running_vserver['state'] == 'UP']:
                res.update({data['name']: data['cursslvpnusers']})

        return res


class Gateway:
    """Representation of an UA Gateway"""
    def __init__(self, type, location, ip):
        self.parent = 'UA'
        self.type = type
        self.location = location
        self.ip = ip
        self.parser = Parser(self.type)

    @property
    def is_primary(self):
        """
        Query the gateway's API and confirm his master state
            Node state is confirmed by looking at "hacurmasterstate"

        E.G.
        endpoint: GET https://10.255.250.27/nitro/v1/stat/hanode
        result: {
                "errorcode": 0,
                "message": "Done",
                "severity": "NONE",
                "hanode": {
                    "hacurstatus": "YES",
                    "hacurstate": "UP",
                    "hacurmasterstate": "Primary",
                    "transtime": "Mon Feb 14 14:29:33 2022",
                    "hatotpktrx": "49020739",
                    "hapktrxrate": 5,
                    "hatotpkttx": "98040405",
                    "hapkttxrate": 10,
                    "haerrproptimeout": "0",
                    "haerrsyncfailure": "0"
                }
            }

        :return bool
        """
        urllib3.disable_warnings()
        try:
            LOGGER.info(f'Querying Gateway {self.ip} Endpoint: GET /nitro/v1/stat/hanode')
            return str(requests.get(f'https://{self.ip}/nitro/v1/stat/hanode',
                                    headers=AUTH_HEADERS,
                                    verify=False,
                                    timeout=10).json()['hanode']['hacurmasterstate']) == 'Primary'
        except Timeout:
            LOGGER.error(f'Gateway {self.ip} fail to connect: Connection timed out (10sec)')
        except Exception as e:
            LOGGER.error(f'Gateway {self.ip} error: {str(e)}')
            return False

    @property
    def current_session_count(self):
        """
        Query the gateway's API to collect their AAA stat.
         return their currently used session count based on their type

        E.G. (default parser)
        endpoint: GET https://10.255.250.27/nitro/v1/stat/aaa
        result: {
                "errorcode": 0,
                "message": "Done",
                "severity": "NONE",
                "aaa": {
                    "aaaauthsuccess": "232978",
                    "aaaauthsuccessrate": 0,
                    "aaaauthfail": "24520",
                    "aaaauthfailrate": 0,
                    "aaaauthonlyhttpsuccess": "104188744",
                    "aaaauthonlyhttpsuccessrate": 5,
                    "aaaauthonlyhttpfail": "0",
                    "aaaauthonlyhttpfailrate": 0,
                    "aaaauthnonhttpsuccess": "862926234",
                    "aaaauthnonhttpsuccessrate": 56,
                    "aaaauthnonhttpfail": "0",
                    "aaaauthnonhttpfailrate": 0,
                    "aaacursessions": "191",
                    "aaacursessionsrate": 0,
                    "aaatotsessions": "215166",
                    "aaasessionsrate": 0,
                    "aaatotsessiontimeout": "132156",
                    "aaasessiontimeoutrate": 0,
                    "aaacuricasessions": "0",
                    "aaacuricasessionsrate": 0,
                    "aaacuricaonlyconn": "0",
                    "aaacuricaonlyconnrate": 0,
                    "aaacuricaconn": "0",
                    "aaacuricaconnrate": 0,
                    "aaacurtmsessions": "0",
                    "aaacurtmsessionsrate": 0,
                    "aaatottmsessions": "0",
                    "aaatmsessionsrate": 0
                }
            }

        :return int
        """
        urllib3.disable_warnings()
        try:
            LOGGER.info(f'Querying Gateway {self.ip} Endpoint: GET /nitro/v1/stat/aaa')
            gateway_stats = requests.get(f'https://{self.ip}/nitro/v1/stat/aaa',
                                         headers=AUTH_HEADERS,
                                         verify=False,
                                         timeout=10).json()
            session_count = self.parser.aaa_parse_strategy(gateway_stats)
            return session_count
        except Timeout:
            LOGGER.error(f'Gateway {self.ip} fail to connect: Connection timed out (10sec)')
        except Exception as e:
            LOGGER.info(f'Gateway {self.ip} error: {str(e)}')
            return 0

    @property
    def detailed_session_count(self):
        """
        Query the gateway's API to collect their VPN VSERVER stat.
         return their currently used session count based on their type per vserver name

        E.G.: (UA Connect parser)
        endpoint: GET https://10.255.250.27/nitro/v1/stat/vpnvserver
        result: {
                "errorcode": 0,
                "message": "Done",
                "severity": "NONE",
                "vpnvserver": [
                    {
                        "name": "connect.ua",
                        "primaryipaddress": "64.254.22.250",
                        "primaryport": 443,
                        "type": "SSL",
                        "state": "UP",
                        "totalrequests": "0",
                        "requestsrate": 0,
                        "totalresponses": "0",
                        "responsesrate": 0,
                        "totalrequestbytes": "0",
                        "requestbytesrate": 0,
                        "totalresponsebytes": "0",
                        "responsebytesrate": 0,
                        "curtotalvpnusers": "0",
                        "cursslvpnusers": "1812"
                    },
                ...

        :return dict
        """
        urllib3.disable_warnings()
        try:
            LOGGER.info(f'Querying Gateway {self.ip} Endpoint: GET /nitro/v1/stat/vpnvserver')
            gateway_stats = requests.get(f'https://{self.ip}/nitro/v1/stat/vpnvserver',
                                         headers=AUTH_HEADERS,
                                         verify=False,
                                         timeout=10).json()
            session_count = self.parser.vserver_parse_strategy(gateway_stats)
            return session_count
        except Timeout:
            LOGGER.error(f'Gateway {self.ip} fail to connect: Connection timed out (10sec)')
        except Exception as e:
            LOGGER.error(f'Gateway {self.ip} error: {str(e)}')
            return 0
