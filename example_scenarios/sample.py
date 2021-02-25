import sys
import requests

'''
  This sample code illustrates how to create, change, check and remove the subscription by calling EnGenius Cloud API.
  Before running this code, please make sure you have an API key generated under your account.
'''

# Modify the following values with yours.
api_key = "YOUR_APIKEY"               # The API Key of the account
org_name = "Test Org"                 # The organization of the account
network_name = "Test Network"         # The network of the organization
ssid_name = "Test SSID"               # The SSID of the network
ssid_passphrase = "YOUR_PASSPHRASE"   # The passphrase of the SSID
serial_number = "YOUR_SERIAL_NUMBER"  # The serial number of the AP
client_mac = "YOUR_CLIENT_MAC"        # The mac of the client

# The prefix of EnGenius Cloud API URL
base_url = "https://falcon.production.engenius.ai/v2"

# Each API call must be with the API Key in the header.
headers = {
    "api-key": api_key
}


print("Create Organization")
create_org_url = base_url + "/orgs"
body = {
    "name": org_name,
    "country": "USA",
    "license_mode": "enterprise",
    "time_zone": "America/Los_Angeles"
}
try:
    response = requests.post(create_org_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)

org_id = response.json().get("id")
hv_id = response.json().get("root_hierarchy_view").get("id")


print("Create Network")
create_network_url = base_url + "/orgs/{}/hvs/{}/networks".format(org_id, hv_id)
body = {
    "name": network_name,
    "country": "USA",
    "time_zone": "America/Los_Angeles"
}
try:
    response = requests.post(create_network_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)

network_id = response.json().get("id")


print("Add Device to Inventory by Serial Number")
add_inventory_url = base_url + "/orgs/{}/inventory".format(org_id)
body = [
    {
        "serial_number": serial_number
    }
]
try:
    response = requests.post(add_inventory_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)

device_id = response.json()[0].get("device_id")
device_mac = response.json()[0].get("mac")


print("Assign Device to Network")
add_device_to_network_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices".format(org_id, hv_id, network_id)
body = [
    {
        "id": device_id
    }
]
try:
    response = requests.post(add_device_to_network_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Create SSID")
create_ssid_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles".format(org_id, hv_id, network_id)
body = {
    "is_enable": True,
    "ssid_types": [
        {
            "type": "2_4G",
            "is_enable": True
        },
        {
            "type": "5G",
            "is_enable": True
        }
    ],
    "ssid_name": ssid_name,
    "security": {
        "auth_type": "WPA2-PSK",
        "wpa": {
            "passphrase": ssid_passphrase,
            "type": "aes",
            "interval": 3600
        }
    }
}
try:
    response = requests.post(create_ssid_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)

ssid_profile_id = response.json().get("id")
ssid_id = response.json().get("ssid_types")[0].get("id")


print("Enable 5G Mesh and Change Channel Width to 80")
update_radio_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps".format(org_id, hv_id, network_id)
body = {
    "radios": [
        {
            "type": "5G",
            "ht_mode": "80",
            "is_mesh_enable": True
        }
    ]
}
try:
    response = requests.patch(update_radio_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Disable Application Analysis")
patch_ssid_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles/{}".format(org_id, hv_id, network_id, ssid_profile_id)
body = {
    "is_app_detection": False
}
try:
    response = requests.patch(patch_ssid_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Get AP Table and Mesh Link Signal Strength")
get_ap_table_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/aps".format(org_id, hv_id, network_id)
try:
    response = requests.get(get_ap_table_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Get SSID Profiles")
get_ssid_profiles_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles".format(org_id, hv_id, network_id)
try:
    response = requests.get(get_ssid_profiles_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Get SSID Number of Clients")
get_ssid_clients_url = base_url + "/orgs/{}/hvs/{}/networks/{}/statistics/ssids".format(org_id, hv_id, network_id)
payload = {"ssid_ids": str([ssid_id])}
try:
    response = requests.get(get_ssid_clients_url, headers=headers, params=payload)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Get Client Ban List")
get_client_ban_list_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/acls/clients".format(org_id, hv_id, network_id)
payload = {"access": "block"}
try:
    response = requests.get(get_client_ban_list_url, headers=headers, params=payload)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Get Network APs Status and Clients Count")
get_ap_status_url = base_url + "/orgs/{}/hvs/{}/networks/{}/radars".format(org_id, hv_id, network_id)
try:
    response = requests.get(get_ap_status_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Get Client Table")
get_clients_url = base_url + "/orgs/{}/hvs/{}/networks/{}/statistics/clients".format(org_id, hv_id, network_id)
try:
    response = requests.get(get_clients_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Change SSID Name and Password")
patch_ssid_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles/{}".format(org_id, hv_id, network_id, ssid_profile_id)
body = {
    "ssid_name": "Change SSID name",
    "security": {
        "wpa": {
            "passphrase": "TestPassphrase"
        }
    }

}
try:
    response = requests.patch(patch_ssid_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Set AP Radio Channel")
update_radio_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps".format(org_id, hv_id, network_id)
body = {
    "radios": [
        {
            "type": "2_4G",
            "channel": "auto"
        },
        {
            "type": "5G",
            "channel": "auto"
        }
    ]
}
try:
    response = requests.patch(update_radio_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("AP Reboot")
ap_reboot_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/{}/reboot".format(org_id, hv_id, network_id, device_id)
try:
    response = requests.get(ap_reboot_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Disable WiFi")
disable_wifi_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps".format(org_id, hv_id, network_id)
body = {
    "radios": [
        {
            "type": "2_4G",
            "is_enable": False
        },
        {
            "type": "5G",
            "is_enable": False
        }
    ]
}
try:
    response = requests.patch(disable_wifi_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Ban Client")
ban_client_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/acls/clients".format(org_id, hv_id, network_id)
body = {
    "mac": client_mac,
    "scope": "network",
    "access": "block"
}
try:
    response = requests.post(ban_client_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Unban Client")
unban_client_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/acls/clients".format(org_id, hv_id, network_id)
body = {
    "access": "block",
    "clients": [
        {
            "scope": "network",
            "mac": client_mac
        }
    ]
}
try:
    response = requests.delete(unban_client_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Kick Client")
kick_client_url = base_url + "/orgs/{}/hvs/{}/networks/{}/clients/{}/kicks".format(org_id, hv_id, network_id, client_mac)
body = {
    "ssid_id": ssid_id,
    "ap_mac": device_mac
}
try:
    response = requests.post(kick_client_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Add AP to Inventory")
add_inventory_url = base_url + "/orgs/{}/inventory".format(org_id)
body = [
    {
        "serial_number": serial_number
    }
]
try:
    response = requests.post(add_inventory_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)

device_id = response.json()[0].get("device_id")


print("Assign Device to Network")
add_device_to_network_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices".format(org_id, hv_id, network_id)
body = [
    {
        "id": device_id
    }
]
try:
    response = requests.post(add_device_to_network_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Release AP to Inventory")
remove_ap_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/{}".format(org_id, hv_id, network_id, device_id)
try:
    response = requests.delete(remove_ap_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)


print("Get AP List")
get_ap_list_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/aps".format(org_id, hv_id, network_id)
try:
    response = requests.get(get_ap_list_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)

ap_list = response.json().get("aps")


print("Release all APs to Inventory")
for ap in ap_list:
    ap_id = ap.get("id")
    remove_ap_url = base_url + "/orgs/{}/hvs/{}/networks/{}/devices/{}".format(org_id, hv_id, network_id, ap_id)
    try:
        response = requests.delete(remove_ap_url, headers=headers)
        if response.status_code >= 300:
            print(response.text)
            sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(0)


print("Empty network - name appended  \"- Disconnected\"")
rename_network_url = base_url + "/orgs/{}/hvs/{}/networks/{}".format(org_id, hv_id, network_id)
body = {
    "name": network_name + " - Disconnected"
}
try:
    response = requests.patch(rename_network_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)

print("Done")
