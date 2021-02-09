class ParseNewGDNBridgeDomainConfigCommand:

    def __init__(self, circuit_id, sub_id):
        self._circuit_id = circuit_id
        self._vpn_id = sub_id

    def execute(self, config):
        result = []

        # Return a list of all bridge-domain-circuit- combine with the circuit id
        # as per GDN circuit bd naming convention one should exist for each circuit
        circuit_bd_list = config.find_objects(r'bridge-domain\sbd-circuit-%s' % self._circuit_id)

        for bd in circuit_bd_list:
            # Looks trough the bd list and get his vfi child
            bd_vfi_list = bd.re_search_children(r'vfi')

            # Looks trough the vfi list and get his vpn-id child matching with the received vpn id
            for vfi in bd_vfi_list:
                match = vfi.re_search_children(r'vpn-id %s' % self._vpn_id)

                # if match found return the whole bd grand-parent config slice
                if match:
                    result = config.find_all_children(bd.text)

        return '\n'.join(result)
