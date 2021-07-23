import requests
import json

vlan_list = '''vlan 3500 name PVLAN-toGDN_DNUse
vlan 3501 name PVLAN-ShrdSVC_vlan1431v1433_DNUse
vlan 3502 name PVLAN-ShrdSVC_vlan1432v1434_DNUse
vlan 3510 name PVLAN-CloudG4
vlan 3511 name PVLAN-MTL_CLOUD_VSS01
vlan 3520 name PVLAN-Blue
vlan 3530 name PVLAN-White
vlan 3540 name PVLAN-Corpo
vlan 3545 name PVLAN-Corpo_backup
vlan 3550 name PVLAN-FSG
vlan 3551 name PVLAN-FSG_Internet
vlan 3555 name PVLAN-FSG_backup
vlan 3560 name PVLAN-JH
vlan 3570 name PVLAN-WSIP
vlan 3580 name PVLAN-OTIS
vlan 3590 name PVLAN-UTC
vlan 3600 name PVLAN-BellCSB
vlan 3630 name PVLAN-AcxsysInterac
vlan 3650 name PVLAN-ACI_GTOCA_dev
vlan 3660 name PVLAN-Cloud_Backup_vl2340
vlan 3670 name PVLAN-Cloud_Backup_vl2339
vlan 3680 name PVLAN-ABU
vlan 3690 name PVLAN-MSS
vlan 3700 name PVLAN-MSS2
vlan 3710 name PVLAN-GAC
vlan 3794 name VLAN3794TBD
vlan 3800 name VLAN3800TBD'''


def build_list_from_string():
    build_vlan_list = list()
    prompt_split = vlan_list.split('\n')

    for line in prompt_split:
        # extract vlan number
        vlan_word_index = line.find('vlan')
        vlan_number = int(line[vlan_word_index + 5: vlan_word_index + 9])

        # extract vlan name
        vlan_word_index = line.find('name')
        vlan_name = line[vlan_word_index + 5:].lower()

        build_vlan_list.append(dict(number=vlan_number, name=vlan_name))

    return build_vlan_list


def build_vlan(number, name, core_id):
    """Return a dict formatted to be send to GaaS API"""
    return {
        "number": number,
        "core_id": int(core_id),
        "client_id": None,
        "custom_name": True,
        "name": str(name[:32]),
        "sub_net": None,
        "mask": None,
        "purpose": None,
        "description": None
    }


def post_to_gaas_api(vlan: dict):
    url = "http://localhost:8000/api/v1/vlans/"

    payload = json.dumps(vlan)
    headers = {
        'Authorization': 'Bearer %s' % api_token,
        'Content-Type': 'application/json'
    }

    print(payload)

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def get_gaas_token():
    url = "http://localhost:8000/api-token-auth/"

    payload = json.dumps({
        "username": "vincent.corriveau",
        "password": "!Abi16Bert18"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


if __name__ == "__main__":
    vlans = build_list_from_string()
    api_token = get_gaas_token().get('token')

    for vlan in vlans:
        body_obj = build_vlan(vlan.get('number'), vlan.get('name'), 17)
        post_to_gaas_api(body_obj)
