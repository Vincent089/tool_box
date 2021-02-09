from net_tools.config_parser.classes.device import Device

old_gdn_device_list = {Device(hostname='CAMTLCDJ1R100', os='cisco_ios', ip='10.206.254.2'),
                       Device(hostname='CAMTLDIC1R100', os='cisco_ios', ip='10.206.254.1'),
                       Device(hostname='CATORMDC1R100', os='cisco_ios', ip='10.206.254.7'),
                       Device(hostname='CATORMDC1R200', os='cisco_ios', ip='10.206.254.8'),
                       Device(hostname='CAOTTBLA1R100', os='cisco_ios', ip='10.206.254.5'),
                       Device(hostname='CAOTTBLA1R200', os='cisco_ios', ip='10.206.254.6')}

new_gdn_device_list = {Device(hostname='CAMTLDIC1R500', os='cisco_xr', ip='10.206.254.3'),
                       Device(hostname='CAMTLDIC1R600', os='cisco_xr', ip='10.206.254.4'),
                       Device(hostname='CAMTLVSL1R500', os='cisco_xr', ip='10.206.254.26'),
                       Device(hostname='CAMTLVSL1R600', os='cisco_xr', ip='10.206.254.27'),
                       Device(hostname='CATORMDC1R500', os='cisco_xr', ip='10.206.254.10'),
                       Device(hostname='CATORMDC1R600', os='cisco_xr', ip='10.206.254.9'),
                       Device(hostname='CASAGSDC1R300', os='cisco_xr', ip='10.206.254.21'),
                       Device(hostname='CASAGSDC1R400', os='cisco_xr', ip='10.206.254.22'),
                       Device(hostname='CAREGDC1R300', os='cisco_xr', ip='10.206.254.19'),
                       Device(hostname='CAREGDC1R400', os='cisco_xr', ip='10.206.254.20'),
                       Device(hostname='USPHXSOU1R100', os='cisco_ios', ip='10.206.254.17'),
                       Device(hostname='USPHXSOU1R200', os='cisco_ios', ip='10.206.254.18')}

gdn_device_list = old_gdn_device_list.union(new_gdn_device_list)
