from ciscoconfparse import CiscoConfParse
from ciscoconfparse.ccp_util import IPv4Obj
from common.string_tool import find_ip_addr_in_string


class Device(object):
    config = None

    def __str__(self):
        return '%s<%s>' % (self.__class__.__name__, self.hostname)

    def __init__(self, hostname, ip, os):
        self.hostname = hostname
        self.ip = ip
        self.os = os

    def get_bridge_domains(self):
        '''
        Read config and extract from l2vpn and bridge group parent all bridge domain infos
        :return:
        '''
        command_name = 'bridge-domains'

        result = {
            command_name: {}
        }

        parse = CiscoConfParse(self.config.splitlines())

        # Return a list of all l2vpn command
        l2vpn_cmds = parse.find_objects('^l2vpn')

        # iterate over the resulting IOSCfgLine objects
        for l2vpn_cmd in l2vpn_cmds:
            # get the bridge group child command from the l2vpn
            for bridge_grp_cmd in l2vpn_cmd.re_search_children(r'^ bridge group '):
                bridge_grp_name = bridge_grp_cmd.text.strip()[len('bridge group '):]

                # get the bridge domain child command from the bridge group
                for bridge_dm_cmd in bridge_grp_cmd.re_search_children(r'^  bridge-domain '):
                    # get the bridge domain map
                    bridge_dm_name = bridge_dm_cmd.text.strip()[len('bridge-domain '):]
                    result[command_name][bridge_dm_name] = {
                        'group-name': bridge_grp_name, 'interface': 'not set', 'vfi-name': 'not set',
                        'vpn-id': 'not set', 'neighbors': list()}

                    for cmd in bridge_dm_cmd.re_search_children(r'^   interface '):
                        result[command_name][bridge_dm_name]['interface'] = cmd.text.strip()[len('interface '):]

                    for cmd in bridge_dm_cmd.re_search_children(r'^   vfi '):
                        result[command_name][bridge_dm_name]['vfi-name'] = cmd.text.strip()[len('vfi '):]

                        for child_cmd in cmd.re_search_children(r'^    vpn-id '):
                            result[command_name][bridge_dm_name]['vpn-id'] = child_cmd.text.strip()[len('vpn-id '):]

                        for child_cmd in cmd.re_search_children(r'^    neighbor '):
                            neighbor = {'ip': 'not set', 'pw-id': 'not set', 'pw-class': 'not set'}

                            pseudowire_id_index = child_cmd.text.strip().find('pw-id')
                            neighbor.update({'pw-id': child_cmd.text.strip()[pseudowire_id_index + len('pw-id '):]})

                            # search for neighbor information
                            for l2_child_cmd in child_cmd.re_search_children(r'^     pw-class '):
                                neighbor.update({'pw-class': l2_child_cmd.text.strip()[len('pw-class '):]})

                            # gets all ip address for the neighbor string found
                            match_positions = find_ip_addr_in_string(child_cmd.text.strip()[len('neighbor '):])

                            # extract all the ip
                            for match in match_positions:
                                neighbor.update(
                                    {'ip': child_cmd.text.strip()[len('neighbor '):][match['start']:match['end']]}
                                )

                            result[command_name][bridge_dm_name]['neighbors'].append(neighbor)
        return result

    def get_policy_maps(self):
        command_name = 'policy-maps'

        result = {
            command_name: {}
        }

        parse = CiscoConfParse(self.config.splitlines())

        # Return a list of all policies
        policy_cmds = parse.find_objects('^policy-map')

        # iterate over the resulting IOSCfgLine objects
        for policy_cmd in policy_cmds:
            # get the policy map name (remove the policy command from the configuration line)
            policy_name = policy_cmd.text[len('policy-map '):]
            result[command_name][policy_name] = {}

            # get the class command from the policy
            for cmd in policy_cmd.re_search_children(r'^ class '):
                class_name = cmd.text.strip()[len('class '):]
                result[command_name][policy_name][class_name] = {}

                # search for the class child police commands
                for child_cmd in cmd.re_search_children(r'^  police rate '):
                    result[command_name][policy_name][class_name] = {
                        'rate': 'not set', 'conform-action': 'not set', 'exceed-action': 'not set'}

                    result[command_name][policy_name][class_name]['rate'] = child_cmd.text.strip()[len('police rate '):]

                    for l2_child_cmd in child_cmd.re_search_children(r'^   conform-action '):
                        result[command_name][policy_name][class_name]['conform-action'] = l2_child_cmd.text.strip()[
                                                                                          len('conform-action '):]
                    for l2_child_cmd in child_cmd.re_search_children(r'^   exceed-action '):
                        result[command_name][policy_name][class_name]['exceed-action'] = l2_child_cmd.text.strip()[
                                                                                         len('exceed-action '):]

                # search for the class child shape commands
                for child_cmd in cmd.re_search_children(r'^  shape '):
                    result[command_name][policy_name][class_name] = {'shape': 'not set'}

                    result[command_name][policy_name][class_name]['shape'] = child_cmd.text.strip()[len('shape '):]

        return result

    def get_interfaces(self):
        result = {
            'interfaces': {}
        }

        if self.config:
            parse = CiscoConfParse(self.config.splitlines())

            # Return a list of all interfaces
            interface_cmds = parse.find_objects('^interface')

            # iterate over the resulting IOSCfgLine objects
            for interface_cmd in interface_cmds:
                # get the interface name (remove the interface command from the configuration line)
                intf_name = interface_cmd.text[len('interface '):]
                result['interfaces'][intf_name] = {}

                # search for the description command, if not set use 'not set' as value
                result['interfaces'][intf_name]['description'] = 'not set'
                for cmd in interface_cmd.re_search_children(r'^ description '):
                    result['interfaces'][intf_name]['description'] = cmd.text.strip()[len('description '):]

                # search for the encapsulation command, if not set use 'not set' as value
                result['interfaces'][intf_name]['encapsulation'] = 'not set'
                for cmd in interface_cmd.re_search_children(r'^ encapsulation '):
                    result['interfaces'][intf_name]['encapsulation'] = cmd.text.strip()[len('encapsulation '):]

                # search for the rewrite command, if not set use 'not set' as value
                result['interfaces'][intf_name]['rewrite'] = 'not set'
                for cmd in interface_cmd.re_search_children(r'^ rewrite '):
                    result['interfaces'][intf_name]['rewrite'] = cmd.text.strip()[len('rewrite '):]

                # search for service-policy command, if not set use 'not set' as value
                # input command
                result['interfaces'][intf_name]['service-policy'] = {'input': 'not set', 'output': 'not set'}
                for cmd in interface_cmd.re_search_children(r'^ service-policy input '):
                    result['interfaces'][intf_name]['service-policy']['input'] = cmd.text.strip()[
                                                                                 len('service-policy input '):]

                # output command
                for cmd in interface_cmd.re_search_children(r'^ service-policy output '):
                    result['interfaces'][intf_name]['service-policy']['output'] = cmd.text.strip()[
                                                                                  len('service-policy output '):]

                # extract IP addresses if defined
                ipv4_regex = r'ip\saddress\s(\S+\s+\S+)'
                for cmd in interface_cmd.re_search_children(ipv4_regex):
                    # ciscoconfparse provides a helper function for this task
                    ipv4_addr = interface_cmd.re_match_iter_typed(ipv4_regex, result_type=IPv4Obj)

                    result['interfaces'][intf_name].update({
                        'ipv4': {
                            'address': ipv4_addr.ip.exploded,
                            'netmask': ipv4_addr.netmask.exploded
                        }
                    })

        return result
