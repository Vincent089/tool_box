import csv
import os
from ipaddr import IPv4Address, IPv4Network
from datetime import datetime
from flask_sse import sse
from bs4 import BeautifulSoup

OUTPUT_PATH = '/src/report_repo'
INPUT_PATH = '/src/input_file'


def broadcast_report_saved(report_name):
    sse.publish({"filename": report_name}, type='new-file')


class CSVDataTransformer:

    def __init__(self, filename):
        self.filename = filename

    def transform(self):
        report_data = []
        data = self._open_file()

        ip_groups = self._extract_group_detail(data=data)

        for ip_group in ip_groups:
            name = ip_group.get('ip_group_name')
            desc = ip_group.get('ip_group_desc')
            speed = ip_group.get('ip_group_speed')
            ips = [dict(source='IPAddress', ips=self._extract_single_ip(group=ip_group)),
                   dict(source='IPNetwork', ips=self._extract_network_ip(group=ip_group)),
                   dict(source='IPRange', ips=self._extract_ip_range(group=ip_group))]

            report_data.append(dict(name=name, desc=desc, speed=speed, ips=ips))

        self._build_csv(data=report_data)
        self._remove_original_input_file()

    def _remove_original_input_file(self):
        os.remove(f'{INPUT_PATH}/{self.filename}')

    def _open_file(self):
        data = open(f'{INPUT_PATH}/{self.filename}', 'r').read()
        return BeautifulSoup(data, 'xml')

    def _extract_group_detail(self, data):
        """Access the XML and extract all groups from IPGroups"""
        return data.find_all('IPGroups')

    def _extract_single_ip(self, group):
        """Access the XML and read child GrpIPAddress and get it only if flag is typed Include
        then return an array out of `addr_id`"""
        results = []
        ip_addresses = group.find_all('GrpIPAddress', {'flag': 'Include'})
        results += [ip_address.get('addr_id') for ip_address in ip_addresses]

        return results

    def _extract_network_ip(self, group):
        """Access the XML and read child GrpIPNetwork and get it only if flag is typed Include
        then return an array of ips fitting in `network_addr_id` and `netmask_addr_id`"""
        results = []
        ip_addresses = group.find_all('GrpIPNetwork', {'flag': 'Include'})

        # for each tag found, makes an IPv4Network object and use his internal function to print out all available IPs
        for ip_address in ip_addresses:
            mask = IPv4Network(ip_address.get('network_addr_id') + '/' + ip_address.get('netmask_addr_id'))
            results += [str(host) for host in mask.iterhosts()]

        return results

    def _extract_ip_range(self, group):
        """Access the XML and read child GrpIPRange and get it only if flag is typed Include
        then makes an range out of `start_addr_id` and `end_addr_id` in order to return an array of all potential IPs"""
        results = []
        ip_address_ranges = group.find_all('GrpIPRange', {'flag': 'Include'})

        # for each tag found, makes an IPv4Network object then within range bound by start_addr_id and end_addr_id
        # print available IPs
        for ip_range in ip_address_ranges:
            results += [str(IPv4Address(ip)) for ip in range(int(IPv4Address(ip_range.get('start_addr_id'))),
                                                             int(IPv4Address(ip_range.get('end_addr_id'))) + 1)]

        return results

    def _build_csv(self, data):
        headers = ['name', 'desc', 'speed', 'ips', 'source']
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        report_name = f'{self.filename[:-4]}-{timestamp}.csv'
        try:
            with open(f'{OUTPUT_PATH}/{report_name}', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()

                for row in data:
                    for source in row.get('ips'):
                        for ip in source.get('ips'):
                            writer.writerow(
                                dict(name=row.get('name'),
                                     desc=row.get('desc'),
                                     speed=row.get('speed'),
                                     source=source.get('source'),
                                     ips=ip))
        except IOError:
            print("I/O error")

        broadcast_report_saved(report_name)
