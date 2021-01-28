class ParseNewGDNInterfaceConfigCommand:

    def __init__(self, circuit_id, sub_id):
        self._circuit_id = circuit_id
        self._vpn_id = sub_id

    def execute(self, config):
        result = []
        found_int_name = []

        # Return a list of all bridge-domain-circuit- combine with the circuit id
        # as per GDN circuit bd naming convention one should exist for each circuit
        circuit_bd_list = config.find_objects(r'bridge-domain\sbd-circuit-%s' % self._circuit_id)

        for bd in circuit_bd_list:
            # Looks trough the bd list and get his interface child
            bd_int_list = bd.re_search_children(r'interface\s+(\S+)')
            found_int_name = [bd_int.text.strip() for bd_int in bd_int_list]

        for int_name in found_int_name:
            result = config.find_all_children('^%s' % int_name)

        return '\n'.join(result)
