import sys
import requests
from calendar import timegm
from datetime import datetime
import os
'''
  This sample code illustrates how to list, add, modify and delete voucher users by calling EnGenius Cloud API.
  Before running this code, please make sure the following:
    1. You have an API key generated under your account.
    2. You have a SSID with voucher service enabled under your organization / network.
    3. You are with admin privilege of this organization / network.
'''

# Modify the following values with yours.
api_key = "YOURAPIKEYHERE"    # The API Key of the account
org_name = "Test Org"         # The organization of the account
network_name = "Test Network" # The network of the organization
ssid_name = "Test SSID"       # The SSID of the network

# The prefix of EnGenius Cloud API URL
base_url = "https://falcon.production.engenius.ai/v2"

# Each API call must be with the API Key in the header.
headers = {
    "api-key": api_key
}

# Get organization list for the account
print("Retrieve organizations...")
get_orgs_url = base_url + "/user/orgs"
try:
    response = requests.get(get_orgs_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)
orgs = response.json()

# Find org_id of this organization
org_id = None
for org in orgs:
    if org["name"] == org_name:
        org_id = org["id"]
        break

if org_id is None:
    print("Cannot find the Org: {}".format(org_name))
    sys.exit(0)

# Get hierarchy views of the organization
print("Retrieve hierarchy views...")
get_hvs_url = base_url + "/orgs/{}/hvs".format(org_id)
try:
    response = requests.get(get_hvs_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)
hvs = response.json()

# Find hv_id, network_id of the network
hv_id = None
network_id = None
for hv in hvs:
    for network in hv["networks"]:
        if network["name"] == network_name:
            hv_id = hv["id"]
            network_id = network["id"]
            break

if network_id is None:
    print("Cannot find the Network: {}".format(network_name))
    sys.exit(0)

# Get SSID profiles
print("Retrieve SSID profiles...")
get_ssid_profiles_url = base_url + "/orgs/{}/hvs/{}/networks/{}/policy/aps/ssid-profiles".format(org_id, hv_id, network_id)
try:
    response = requests.get(get_ssid_profiles_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)
ssid_profiles = response.json()

# Find ssid_profile_id
ssid_profile_id = None
for ssid_profile in ssid_profiles:
    if ssid_profile["ssid_name"] == ssid_name:
        ssid_profile_id = ssid_profile["id"]
        break

if ssid_profile_id is None:
    print("Cannot find the SSID: {}".format(ssid_name))
    sys.exit(0)

print("Create 3 voucher users for EnGenius Cloud RADIUS")
create_engenius_radius_users_v2_url = base_url + "/orgs/{}/hvs/{}/networks/{}/ssid-profiles/{}/engenius-radius-users-v2".format(org_id, hv_id, network_id, ssid_profile_id)
expiration_date = timegm(datetime.utcnow().utctimetuple()) * 1000 + (60 * 60 * 1000) # expire after 1 hour

print('Case 1: create user with auto generated username / password')
body = {
    "is_auto_gen": True,
    "note": "Case 1 - created with auto generated username / password",
    "simultaneous_use": 1,
    "expiration_date": expiration_date
}
try:
    response = requests.post(create_engenius_radius_users_v2_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)
case_1_voucher_user = response.json()

print('Case 2: create user with specific username / password')
body = {
    "is_auto_gen": False,
    "username": "case2_user",
    "password": "123456",
    "note": "Case 2 - created with specific username / password",
    "simultaneous_use": 1,
    "expiration_date": expiration_date
}
try:
    response = requests.post(create_engenius_radius_users_v2_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)
case_2_voucher_user = response.json()

print('Case 3: create user with specific username and auto generated password')
body = {
    "is_auto_gen": False,
    "username": "case3_user",
    "note": "Case 3 - created with specific username",
    "simultaneous_use": 1,
    "expiration_date": expiration_date
}
try:
    response = requests.post(create_engenius_radius_users_v2_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)
case_3_voucher_user = response.json()

# Modify Case 1 user
print("Modify password, simultaneous_use, note and expiration_date for case 1 users")
body = {
    "password": "updated_password",
    "note": "Case 1 - user is updated",
    "simultaneous_use": 2,
    "expiration_date": expiration_date + (60 * 60 * 1000)
}
try:
    update_engenius_radius_users_v2_url = base_url + "/orgs/{}/hvs/{}/networks/{}/ssid-profiles/{}/engenius-radius-users-v2/{}".format(org_id, hv_id, network_id, ssid_profile_id, case_1_voucher_user["id"])
    response = requests.patch(update_engenius_radius_users_v2_url, headers=headers, json=body)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)

# Print voucher users
print("Show all voucher users")
get_engenius_radius_users_v2_url = base_url + "/orgs/{}/hvs/{}/networks/{}/ssid-profiles/{}/engenius-radius-users".format(org_id, hv_id, network_id, ssid_profile_id)
try:
    response = requests.get(get_engenius_radius_users_v2_url, headers=headers)
    if response.status_code >= 300:
        print(response.text)
        sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(0)
voucher_user_list = response.json()

for user in voucher_user_list:
    print("==========================================")
    print("Name: {}".format(user['username']))
    print("Password: {}".format(user['password']))
    print("Expiration Date: {}".format(datetime.utcfromtimestamp(user['expiration_date'] / 1000)))
    print("Simultaneous Login: {}".format(user['access_plan']['simultaneous_use']))
    print("Status: {}".format(user['status']))
    print("Note: {}".format(user['note']))
print("==========================================")

# Finally, delete created users before exiting
print("Delete created users")
for user_id in [ case_1_voucher_user['id'], case_2_voucher_user['id'], case_3_voucher_user['id'] ]:
    del_engenius_radius_users_url = base_url + "/orgs/{}/hvs/{}/networks/{}/ssid-profiles/{}/engenius-radius-users/{}".format(org_id, hv_id, network_id, ssid_profile_id, user_id)
    try:
        response = requests.delete(del_engenius_radius_users_url, headers=headers)
        if response.status_code >= 300:
            print(response.text)
            sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(0)

print("Done")
