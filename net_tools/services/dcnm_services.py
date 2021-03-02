import json

import requests

hdr = {'Accept': 'application/json', 'Content-Type': 'application/json; charset=UTF-8'}
response = requests.post('https://172.27.247.60/rest/logon',
                         data=json.dumps({}),
                         headers=hdr,
                         auth=('vincent.corriveau', ''),
                         timeout=10,
                         verify=False)

session_id = None
if response and (response.status_code == requests.codes.ok):
    session_id = response.json().get('Dcnm-Token')

hdr.update({'Dcnm-Token': session_id})
interfaceUrl = 'https://172.27.247.60/rest/interface'
response = requests.get(interfaceUrl, headers=hdr, verify=False)

if response and (response.status_code == requests.codes.ok):
    interfacePlan = response.json()

    print(interfacePlan)
