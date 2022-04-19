import sys
from requests import request

'''
  This sample code illustrates how to create, change, check and remove the subscription by calling EnGenius Cloud API.
  Before running this code, please make sure you have an API key generated under your account.
'''

# Modify the following values with yours.
api_key = "YOUR_APIKEY"               # The API Key of the account
org_name = "Test Org"                 # The organization of the account
hv_name = "Test HV"                   # The hierarchy view of the organization
network_name = "Test Network"         # The network of the hierarchy view
serial_number = "YOUR_SERIAL_NUMBER"  # The serial number of the device
ssid_name = "Test SSID"               # The SSID of the network
client_mac = "YOUR_CLIENT_MAC"        # The mac of the client

# The prefix of EnGenius Cloud API URL
base_url = "https://falcon.production.engenius.ai/v2"


# Each API call must be with the API Key in the header.
headers = {
    "api-key": api_key
}


def send_request(method, url, params=None, json=None, request_headers=None):
    try:
        resp = request(method, url, params=params, json=json, headers=request_headers)
        if resp.status_code >= 300:
            print(resp.json())
    except Exception as e:
        print(e)
        sys.exit(0)
    return resp


print("Create a new organization")
create_org_url = base_url + "/orgs"
body = {
    "name": org_name,
    "country": "USA",
    "time_zone": "America/Los_Angeles"
}
response = send_request("POST", create_org_url, request_headers=headers, json=body)

org_id = response.json().get("id")
root_hv_id = response.json().get("root_hierarchy_view").get("id")


print("Get all the organizations that the user has privileges on")
get_orgs_url = base_url + "/user/orgs"
response = send_request("GET", get_orgs_url, request_headers=headers)


print("Get all the networks that the user has privileges on (for Front-desk Portal)")
get_networks_url = base_url + "/user/frontdesk-portal"
response = send_request("GET", get_networks_url, request_headers=headers)


print("Get the organization")
get_org_url = base_url + "/orgs/{}".format(org_id)
response = send_request("GET", get_org_url, request_headers=headers)


print("Update the organization")
patch_org_url = base_url + "/orgs/{}".format(org_id)
body = {
    "ap_license_mode": "pro"
}
response = send_request("PATCH", patch_org_url, request_headers=headers, json=body)


print("Register devices in the organization")
register_device_url = base_url + "/orgs/{}/inventory".format(org_id)
body = [
    {
        "serial_number": serial_number
    }
]
response = send_request("POST", register_device_url, request_headers=headers, json=body)

device_id = response.json()[0].get("device_id")
device_mac = response.json()[0].get("mac")


print("Get all devices in the organization")
get_inventory_url = base_url + "/orgs/{}/inventory".format(org_id)
response = send_request("GET", get_inventory_url, request_headers=headers)


print("Create a hierarchy view")
create_hv_url = base_url + "/orgs/{}/hvs".format(org_id)
body = {
    "parent_hierarchy_view_id": root_hv_id,
    "name": hv_name
}
response = send_request("POST", create_hv_url, request_headers=headers, json=body)

hv_id = response.json().get("id")


print("Get all hierarchy views that the user has privileges on in an organization")
get_hvs_url = base_url + "/orgs/{}/hvs".format(org_id)
response = send_request("GET", get_hvs_url, request_headers=headers)


print("Get the hierarchy view")
get_hv_url = base_url + "/orgs/{}/hvs/{}".format(org_id, hv_id)
response = send_request("GET", get_hv_url, request_headers=headers)


print("Update the hierarchy view")
patch_hv_url = base_url + "/orgs/{}/hvs/{}".format(org_id, hv_id)
body = {
    "name": hv_name
}
response = send_request("PATCH", patch_hv_url, request_headers=headers, json=body)


print("Get the client's journey in the hierarchy view")
get_hv_client_journey_url = base_url + "/orgs/{}/hvs/{}/clients/{}/journey".format(org_id, hv_id, client_mac)
response = send_request("GET", get_hv_client_journey_url, request_headers=headers)


print("Get all switches in the hierarchy view")
get_hv_switches_url = base_url + "/orgs/{}/hvs/{}/devices/switches".format(org_id, hv_id)
response = send_request("GET", get_hv_switches_url, request_headers=headers)


print("Get all clients in the hierarchy view")
get_hv_clients_url = base_url + "/orgs/{}/hvs/{}/statistics/clients".format(org_id, hv_id)
response = send_request("GET", get_hv_clients_url, request_headers=headers)


print("Create a network")
create_network_url = base_url + "/orgs/{}/hvs/{}/networks".format(org_id, hv_id)
body = {
    "name": network_name,
    "country": "USA",
    "time_zone": "America/Los_Angeles"
}
response = send_request("POST", create_network_url, request_headers=headers, json=body)

network_id = response.json().get("id")


print("Get the network")
get_network_url = base_url + "/orgs/{}/hvs/{}/networks/{}".format(org_id, hv_id, network_id)
response = send_request("GET", get_network_url, request_headers=headers)


print("Update the network")
patch_network_url = base_url + "/orgs/{}/hvs/{}/networks/{}".format(org_id, hv_id, network_id)
body = {
    "name": network_name
}
response = send_request("PATCH", patch_network_url, request_headers=headers, json=body)


print("Get the client's journey in the network")
get_network_client_journey_url = base_url + "/orgs/{}/hvs/{}/networks/{}/clients/{}/journey".format(org_id, hv_id, network_id, client_mac)
response = send_request("GET", get_network_client_journey_url, request_headers=headers)


print("Assign the device to the network")
assign_device_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices".format(org_id, hv_id, network_id)
body = [
    {
        "id": device_id
    }
]
response = send_request("POST", assign_device_url, request_headers=headers, json=body)


print("Kick the client of the device in the network")
kick_network_client_url = base_url + "/orgs/{}/hvs/{}/networks/{}/clients/{}/kicks".format(org_id, hv_id, network_id, client_mac)
body = {
    "ssid_id": 0,
    "ap_mac": device_mac
}
response = send_request("POST", kick_network_client_url, request_headers=headers, json=body)


print("Get all APs in the network")
get_network_aps_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/aps".format(org_id, hv_id, network_id)
response = send_request("GET", get_network_aps_url, request_headers=headers)


print("Get all switches in the network")
get_network_switches_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/switches".format(org_id, hv_id, network_id)
response = send_request("GET", get_network_switches_url, request_headers=headers)


print("Get the AP related settings for the network")
get_network_ap_policy_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps".format(org_id, hv_id, network_id)
response = send_request("GET", get_network_ap_policy_url, request_headers=headers)


print("Update the AP related settings for the network")
patch_network_ap_policy_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps".format(org_id, hv_id, network_id)
body = {
    "radios": [
        {
            "type": "2_4G",
            "channel": "auto"
        }
    ]
}
response = send_request("PATCH", patch_network_ap_policy_url, request_headers=headers, json=body)


print("Add a client to L2 ACL block/VIP list in the network or SSID")
add_network_acl_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/acls/clients".format(org_id, hv_id, network_id)
body = {
    "mac": client_mac,
    "scope": "network",
    "access": "block"
}
response = send_request("POST", add_network_acl_url, request_headers=headers, json=body)


print("Get L2 ACL block/VIP list in the network and SSID")
get_network_acl_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/acls/clients".format(org_id, hv_id, network_id)
payload = {"access": "vip"}
response = send_request("GET", get_network_acl_url, request_headers=headers, params=payload)


print("Delete clients from L2 ACL block/VIP list in the network or SSID")
delete_network_acl_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/acls/clients".format(org_id, hv_id, network_id)
body = {
    "access": "block",
    "clients": [
        {
            "scope": "network",
            "mac": client_mac
        }
    ]
}
response = send_request("DELETE", delete_network_acl_url, request_headers=headers, json=body)


print("Create a SSID profile in the network")
create_ssid_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles".format(org_id, hv_id, network_id)
body = {
    "ssid_name": ssid_name,
    "ssid_category": "General",
    "ssid_types": [
        {
            "type": "2_4G",
            "is_enable": True
        },
        {
            "type": "5G",
            "is_enable": True
        }
    ]
}
response = send_request("POST", create_ssid_url, request_headers=headers, json=body)

ssid_profile_id = response.json().get("id")


print("Get all SSID profiles in the network")
get_ssids_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles".format(org_id, hv_id, network_id)
response = send_request("GET", get_ssids_url, request_headers=headers)


print("Get the SSID profile in the network")
get_ssid_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles/{}".format(org_id, hv_id, network_id, ssid_profile_id)
response = send_request("GET", get_ssid_url, request_headers=headers)


print("Update the SSID profile in the network")
patch_ssid_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles/{}".format(org_id, hv_id, network_id, ssid_profile_id)
body = {
    "ssid_name": ssid_name
}
response = send_request("PATCH", patch_ssid_url, request_headers=headers, json=body)


print("Get the switch related settings for the network")
get_network_switch_policy_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/switches".format(org_id, hv_id, network_id)
response = send_request("GET", get_network_switch_policy_url, request_headers=headers)


print("Update the switch related settings for the network")
patch_network_switch_policy_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/switches".format(org_id, hv_id, network_id)
body = {
    "lldp": {
        "is_enable": True
    }
}
response = send_request("PATCH", patch_network_switch_policy_url, request_headers=headers, json=body)


print("Create a VLAN profile in the network")
create_vlan_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/vlans".format(org_id, hv_id, network_id)
body = {
    "id": 100,
    "name": "VLAN 100"
}
response = send_request("POST", create_vlan_url, request_headers=headers, json=body)


print("Get all VLAN profiles in the network")
get_vlans_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/vlans".format(org_id, hv_id, network_id)
response = send_request("GET", get_vlans_url, request_headers=headers)


print("Update the VLAN profile in the network")
patch_vlan_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/vlans/{}".format(org_id, hv_id, network_id, 100)
body = {
    "name": "default"
}
response = send_request("PATCH", patch_vlan_url, request_headers=headers, json=body)


print("Delete the VLAN profile in the network")
delete_vlan_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/vlans/{}".format(org_id, hv_id, network_id, 100)
response = send_request("DELETE", delete_vlan_url, request_headers=headers)


print("Get the radar analysis data of the network")
get_network_radar_url = base_url + "/orgs/{}/hvs/{}/networks/{}/radar".format(org_id, hv_id, network_id)
response = send_request("GET", get_network_radar_url, request_headers=headers)


print("Get all Bluetooth clients in the network")
get_network_bluetooth_clients_url = base_url + "/orgs/{}/hvs/{}/networks/{}/statistics/ble-clients".format(org_id, hv_id, network_id)
response = send_request("GET", get_network_bluetooth_clients_url, request_headers=headers)


print("Get all clients in the network")
get_network_clients_url = base_url + "/orgs/{}/hvs/{}/networks/{}/statistics/clients".format(org_id, hv_id, network_id)
response = send_request("GET", get_network_clients_url, request_headers=headers)


print("Get traffic analysis data of all SSIDs in the network")
get_network_ssid_traffic_url = base_url + "/orgs/{}/hvs/{}/networks/{}/statistics/ssids".format(org_id, hv_id, network_id)
payload = {"ssid_ids": "[0]"}
response = send_request("GET", get_network_ssid_traffic_url, request_headers=headers, params=payload)


print("Reboot the device in the network")
reboot_network_device_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/{}/reboot".format(org_id, hv_id, network_id, device_id)
response = send_request("GET", reboot_network_device_url, request_headers=headers)


print("Get the AP in the network")
get_network_ap_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/aps/{}".format(org_id, hv_id, network_id, device_id)
response = send_request("GET", get_network_ap_url, request_headers=headers)


print("Update the settings of the AP in the network")
patch_network_ap_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/aps/{}".format(org_id, hv_id, network_id, device_id)
body = {
    "config": {
        "led_setting": {
            "is_override": False
        }
    }
}
response = send_request("PATCH", patch_network_ap_url, request_headers=headers, json=body)


print("Get all clients of the AP in the network")
get_network_device_clients_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/aps/{}/clients".format(org_id, hv_id, network_id, device_id)
response = send_request("GET", get_network_device_clients_url, request_headers=headers)


print("Get the switch in the network")
get_network_switch_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/switches/{}".format(org_id, hv_id, network_id, device_id)
response = send_request("GET", get_network_switch_url, request_headers=headers)


print("Update the settings of the switch in the network")
patch_network_switch_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/switches/{}".format(org_id, hv_id, network_id, device_id)
body = {
    "config": {
        "led_setting": {
            "is_override": False
        }
    }
}
response = send_request("PATCH", patch_network_switch_url, request_headers=headers, json=body)


print("Get the link aggregation settings of the switch in the network")
get_network_switch_trunk_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/switches/{}/link-aggregations".format(org_id, hv_id, network_id, device_id)
response = send_request("GET", get_network_switch_trunk_url, request_headers=headers)


print("Update the link aggregation settings of the switch in the network")
put_network_switch_trunk_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/switches/{}/link-aggregations".format(org_id, hv_id, network_id, device_id)
body = [
    {
        "id": 1,
        "mode": "disabled",
        "members": []
    }
]
response = send_request("PUT", put_network_switch_trunk_url, request_headers=headers, json=body)


print("Get the mirror settings of the switch in the network")
get_network_switch_mirror_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/switches/{}/mirrors".format(org_id, hv_id, network_id, device_id)
response = send_request("GET", get_network_switch_mirror_url, request_headers=headers)


print("Update the mirror settings of the switch in the network")
put_network_switch_mirror_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/switches/{}/mirrors".format(org_id, hv_id, network_id, device_id)
body = [
    {
        "id": 1,
        "is_enable": False
    }
]
response = send_request("PUT", put_network_switch_mirror_url, request_headers=headers, json=body)


print("Update the port settings of the switch in the network")
patch_network_switch_ports_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/switches/{}/ports".format(org_id, hv_id, network_id, device_id)
body = {
    "ports": ["1"],
    "is_enable": True
}
response = send_request("PATCH", patch_network_switch_ports_url, request_headers=headers, json=body)


print("Create MyPSK users in the network")
create_network_mypsk_users_url = base_url + "/orgs/{}/hvs/{}/networks/{}/engenius-mypsk-users".format(org_id, hv_id, network_id)
body = {
    "is_auto_gen": True,
    "passphrase_count": 1,  # numbers of auto generated MyPSK users
    "passphrase_length": 8,
    "vlan_id": 0  # 0: SSID's VLAN
}
response = send_request("POST", create_network_mypsk_users_url, request_headers=headers, json=body)

mypsk_user_id = response.json().get("mypsk_users")[0].get("id")


print("Get all MyPSK users in the network")
get_network_mypsk_users_url = base_url + "/orgs/{}/hvs/{}/networks/{}/engenius-mypsk-users".format(org_id, hv_id, network_id)
response = send_request("GET", get_network_mypsk_users_url, request_headers=headers)


print("Update MyPSK users in the network")
patch_network_mypsk_users_url = base_url + "/orgs/{}/hvs/{}/networks/{}/engenius-mypsk-users".format(org_id, hv_id, network_id)
body = {
    "ids": [mypsk_user_id],
    "status": "enabled"
}
response = send_request("PATCH", patch_network_mypsk_users_url, request_headers=headers, json=body)


print("Delete MyPSK users in the network")
delete_network_mypsk_users_url = base_url + "/orgs/{}/hvs/{}/networks/{}/engenius-mypsk-users".format(org_id, hv_id, network_id)
body = [mypsk_user_id]
response = send_request("DELETE", delete_network_mypsk_users_url, request_headers=headers, json=body)


print("Create an voucher user for EnGenius Cloud RADIUS of the SSID in the network")
create_voucher_user_url = base_url + "/orgs/{}/hvs/{}/networks/{}/ssid-profiles/{}/engenius-radius-users-v2".format(org_id, hv_id, network_id, ssid_profile_id)
body = {
    "is_auto_gen": True,
    "simultaneous_use": 1,
    "expiration_date": 1672416000000
}
response = send_request("POST", create_voucher_user_url, request_headers=headers, json=body)

engenius_voucher_user_id = response.json().get("id")


print("Get all voucher users for EnGenius Cloud RADIUS of the SSID in the network")
get_voucher_users_url = base_url + "/orgs/{}/hvs/{}/networks/{}/ssid-profiles/{}/engenius-radius-users".format(org_id, hv_id, network_id, ssid_profile_id)
response = send_request("GET", get_voucher_users_url, request_headers=headers, json=body)


print("Update the voucher user for EnGenius Cloud RADIUS of the SSID in the network")
patch_voucher_user_url = base_url + "/orgs/{}/hvs/{}/networks/{}/ssid-profiles/{}/engenius-radius-users-v2/{}".format(org_id, hv_id, network_id, ssid_profile_id, engenius_voucher_user_id)
body = {
    "simultaneous_use": 1
}
response = send_request("PATCH", patch_voucher_user_url, request_headers=headers, json=body)


print("Delete the voucher user for EnGenius Cloud RADIUS of the SSID in the network")
delete_voucher_user_url = base_url + "/orgs/{}/hvs/{}/networks/{}/ssid-profiles/{}/engenius-radius-users/{}".format(org_id, hv_id, network_id, ssid_profile_id, engenius_voucher_user_id)
response = send_request("DELETE", delete_voucher_user_url, request_headers=headers)


print("Delete the SSID profile in the network")
delete_ssid_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles/{}".format(org_id, hv_id, network_id, ssid_profile_id)
response = send_request("DELETE", delete_ssid_url, request_headers=headers)


print("Remove the device from the network")
delete_network_device_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/{}".format(org_id, hv_id, network_id, device_id)
response = send_request("DELETE", delete_network_device_url, request_headers=headers)


print("Remove devices from corresponding networks")
delete_networks_devices_url = base_url + "/orgs/{}/devices".format(org_id)
body = [
    {
        "device_id": device_id,
        "network_id": network_id
    }
]
response = send_request("DELETE", delete_networks_devices_url, request_headers=headers, json=body)


print("Delete the network")
delete_network_url = base_url + "/orgs/{}/hvs/{}/networks/{}".format(org_id, hv_id, network_id)
response = send_request("DELETE", delete_network_url, request_headers=headers)


print("Delete the hierarchy view")
delete_hv_url = base_url + "/orgs/{}/hvs/{}".format(org_id, hv_id)
response = send_request("DELETE", delete_hv_url, request_headers=headers)


print("Deregister the device from the organization")
deregister_device_url = base_url + "/orgs/{}/inventory/{}".format(org_id, device_id)
response = send_request("DELETE", deregister_device_url, request_headers=headers)


print("Delete the organization")
delete_org_url = base_url + "/orgs/{}".format(org_id)
response = send_request("DELETE", delete_org_url, request_headers=headers)


print("Done")
