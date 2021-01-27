import json
from common.csv_tool import build_csv_with_headers


class Vlan:
    def __init__(self, number: int):
        self.number = number


class CircuitSubCircuit:
    """
    A GDN Subcircuit
    """

    def __init__(self, number: int, vlans=None):
        self.number = number
        self.vlans = vlans

    def add_vlan(self, vlan):
        self.vlans.append(vlan)


class Circuit:
    """
    A GDN circuit
    """

    def __init__(self, number: int, description: str, speed: int, path: str, sub_circuits=None):
        self.number = number
        self.desc = description
        self.speed = speed
        self.sub_circuits = sub_circuits
        self.path = path

    def add_sub_circuit(self, sub_circuit: CircuitSubCircuit):
        self.sub_circuits.append(sub_circuit)


def load_file(file_location: str):
    """
    Load a json file into the script
    :param file_location:
    :return:
    """
    with open(file_location) as jsonFile:
        print('\nFile data loaded')

        data = json.load(jsonFile)

    return data


def map_data(json_data):
    circuits = []

    for circuit_sub_circuit_number in json_data:
        path = []
        circuit_number = None
        circuit_speed = None
        circuit_desc = None
        circuit_vlan_numbers = []

        for key, values in json_data.get(circuit_sub_circuit_number).items():

            # device key which contains the device name and extract his location
            device_path_hook = key[2:5]
            if device_path_hook not in path:
                path.append(device_path_hook)

            for key, values in values.items():

                if key == 'bridge-domains':
                    for element in values:
                        for inner_key, inner_values in element.items():
                            # extract from key circuit number
                            key_word_len = len(r'bd-circuit-')
                            circuit_number = inner_key[key_word_len:key_word_len + 4]

                            # extract from interface the vlan number
                            separator_index = inner_values.get('interface').find('.')
                            vlan_number = inner_values.get('interface')[separator_index + 1:]
                            if vlan_number is not None:
                                if vlan_number not in circuit_vlan_numbers:
                                    circuit_vlan_numbers.append(vlan_number)

                if key == 'interfaces':
                    for element in values:
                        for inner_key, inner_values in element.items():
                            circuit_desc = inner_values.get('description')

                if key == 'policy-maps':
                    for element in values:
                        for inner_key, inner_values in element.items():
                            key_word_len = len(r'circuit_bandwidth_')
                            key_found_index = inner_key[key_word_len:].find('M')
                            circuit_speed = inner_key[key_word_len:key_word_len + key_found_index]

        # create a new sub circuit with all his vlans
        new_sub_circuit = CircuitSubCircuit(number=circuit_sub_circuit_number,
                                            vlans=[Vlan(vlan_number) for vlan_number in circuit_vlan_numbers])

        # create a new circuit with his sub circuit
        new_circuit = Circuit(number=circuit_number,
                              description=circuit_desc,
                              speed=circuit_speed,
                              path='-'.join(path),
                              sub_circuits=[new_sub_circuit])

        # try to find new circuit in the stored list, if found update his sub circuits
        found = False
        for circuit in circuits:
            if circuit.number == new_circuit.number:
                circuit.add_sub_circuit(new_sub_circuit)
                found = True
                break

        if not found:
            circuits.append(new_circuit)

    return circuits


def main():
    """Entry point"""
    # file_location = input('Enter your json file path : ')
    file_location = r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_output\gdn_circuit_map.json'

    file_data = load_file(file_location)
    circuits = map_data(file_data)

    circuits.sort(key=lambda item: item.number)

    build_csv_with_headers(
        file_name='circuit_mapper',
        file_headers=['number', 'desc', 'speed', 'path', 'subcircuits'],
        file_rows=[{'number': circuit.number,
                    'desc': circuit.desc,
                    'speed': circuit.speed,
                    'path': circuit.path,
                    'subcircuits': [sub.number for sub in circuit.sub_circuits]} for
                   circuit in circuits])

    # for circuit in circuits:
    #     print('Circuit #%s Desc.:%s' % (circuit.number, circuit.desc))
    #
    #     for sub in circuit.sub_circuits:
    #         print('\tSubcircuit #%s vlans:%s' % (sub.number, [vlan.number for vlan in sub.vlans]))

    # print(len(circuits))


if __name__ == "__main__":
    import doctest

    doctest.testmod(main())
