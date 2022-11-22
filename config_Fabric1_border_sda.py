import requests
from requests.auth import HTTPBasicAuth
import json
import os
import time
from requests.packages import urllib3
urllib3.disable_warnings()
DNAC_URL = "https://172.16.6.136"
DNAC_USERNAME = "admin"
DNAC_PASSWORD = "Bxbdmz2017!@#$"
API_SUCCESS = 200

#MFK Validated this Function Works
# def dnac_login():
#     url = f"{DNAC_URL}/api/system/v1/auth/token"
#
#     headers = {'content-type': 'application/json'}
#     resp = requests.post(url, auth=HTTPBasicAuth(username=DNAC_USERNAME, password=DNAC_PASSWORD), headers=headers, verify=False)
#     token = resp.json()['Token']
#     print(token)
#
# dnac_login()

def get_token():
    header_dictionary = {'Content-Type': 'application/json', 'Authorization': 'Basic YWRtaW46QnhiZG16MjAxNyFAIyQ='}
    response = requests.post(f'{DNAC_URL}/dna/system/api/v1/auth/token', headers=header_dictionary, verify=False, timeout=60)
    json_dictionary_from_response = response.json()
    token = str(json_dictionary_from_response['Token'])
    return token

# Add VN to SDA: Failed
# {'status': 'failed', 'description': 'Could not find fabric site for given siteNameHierarchy in request. '
#                                     'Provide valid siteNameHierarchy that is fabric site.',
#  'taskId': None, 'taskStatusUrl': '/dna/intent/api/v1/task/null',
#  'executionStatusUrl': '/dna/intent/api/v1/execution-status/dba32c27-4188-48f3-a923-c6c5291a2b2f',
#  'executionId': 'dba32c27-4188-48f3-a923-c6c5291a2b2f'
# Status Code: 200

def addVn():
    headers = {'Content-Type': 'application/json', 'x-auth-token': get_token()}
    payload = [
        {
            # TODO: Variables need to be added
            # "virtualNetworkName": Fabric1_VN,
            "virtualNetworkName": "Fabric1_VN",
            # "siteNameHierarchy": Fabric1_SDA_Fabric_Name
            "siteNameHierarchy": "Global/MultiDomainSite/Fabric1"

        }
    ]
    request = requests.post(f'{DNAC_URL}/dna/intent/api/v1/business/sda/virtual-network', data=json.dumps(payload), headers=headers, verify=False, timeout=60)
    print(request.status_code)
    if request.status_code == 202:
        print ("Add VN to SDA: Passed")
    else:
        print ("Add VN to SDA: Failed")
    json_response = request.json()
    print(json_response)
    return (str(json_response))

addVn()

def get_network_device():
    headers = {'Content-Type': 'application/json', 'x-auth-token': get_token()}
    new_url = DNAC_URL + "/api/v1/network-device"
    payload = None
    # response = requests.request('GET', url, headers=headers, data=payload)
    # request = requests.post(executionStatusUrl,
    #                         data=json.dumps(payload), headers=headers, verify=False, timeout=60)
    response = requests.get(new_url, headers=headers, data=payload, verify=False).json()
    return(response)


    json_response = request.json()
    return (str(json_response))

# def provisionVn():
#     headers = {'Content-Type': 'application/json', 'x-auth-token': get_token()}
#     payload = [
#         {
#             "virtualNetworkName": Fabric1_VN,
#             "ipPoolName": Fabric1_IpPool_Name,
#             "trafficType": "DATA",
#             "authenticationPolicyName": "10_55_55_0-" + Fabric1_VN,
#             "scalableGroupName": "",
#             "isL2FloodingEnabled": False,
#             "isThisCriticalPool": False,
#             "poolType": "Generic"
#         }
#     ]
#     request = requests.post('https://10.85.189.34/dna/intent/api/v1/business/sda/virtualnetwork/ippool', data=json.dumps(payload), headers=headers, verify=False, timeout=60)
#     if request.status_code == 200:
#         print ("Provision VN: Passed")
#     else:
#         print ("Provision VN: Failed")
#     json_response = request.json()
#     return (str(json_response))
#
# def bgpConfig():
#     headers = {'Content-Type': 'application/json', 'x-auth-token': get_token()}
#     payload = {
#         "forcePushTemplate": True,
#         "isComposite": False,
#         "mainTemplateId": "189ee26e-93ac-4e2d-b785-127e06de7282",
#         "targetInfo": [
#             {
#                 "hostName": "MSX-OTT02-ISR4431-07.cisco.com",
#                 "id": "3042af02-2a24-457a-9af4-75f63ebadde9",
#                 "params": {
#                 "VN_NAME": Fabric1_VN,
# 	    	"REMOTE_AS_NUMBER": "65502",
#                 "FUSION_VRF_IP_ADD": Fabric1_SDWAN_VN_Extension_IP,
#                 "VPN_NO": VPN_NO,
#                 "SDA_VN_Extension_IP": Fabric1_SDA_VN_Extension_IP,
# 	    	"AS_NUMBER": "65501"
# 	    	},
#                "type": "MANAGED_DEVICE_UUID"
#            }
#        ],
#        "templateId": "189ee26e-93ac-4e2d-b785-127e06de7282"
#     }
#     request = requests.post('https://10.85.189.34/dna/intent/api/v1/template-programmer/template/deploy', data=json.dumps(payload), headers=headers, verify=False, timeout=60)
#     if request.status_code == 202:
#         print ("BGP Configuration: Passed")
#     else:
#         print ("BGP Configuration: Failed")
#     json_response = request.json()
#     return (str(json_response))
#
# def provisionInt():
#     headers = {'Content-Type': 'application/json', 'x-auth-token': get_token()}
#     payload = [
#         {
#             "siteNameHierarchy": "Global/MultiDomainSite/Fabric1",
#             "deviceManagementIpAddress": "10.85.189.233",
#             "interfaceName": "GigabitEthernet1/0/3",
#             "dataIpAddressPoolName": "Test55Reserve",
#             "voiceIpAddressPoolName": "",
#             "authenticateTemplateName": "No Authentication"
#         }
#     ]
#     request = requests.post('https://10.85.189.34/dna/intent/api/v1/business/sda/hostonboarding/user-device', data=json.dumps(payload), headers=headers, verify=False, timeout=60)
#     if request.status_code == 200:
#         print ("Interface Provision: Passed")
#     else:
#         print ("Interface Provision: Failed")
#     json_response = request.json()
#     return (str(json_response))
#
# Fabric1_VN = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric1 VN Name$]"
# Fabric1_IpPool_Name = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric1 Reserved IP Pool Name$]"
# Fabric1_SDA_Fabric_Name = "Global/MultiDomainSite/" + "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric1 - Fabric Name$]"
# Fabric1_SDWAN_VN_Extension_IP = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric1 SDWAN VN Extension IP. eg; 1.1.1.1$]"
# VPN_NO = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.SDWAN VPN ID$]"
# Fabric1_SDA_VN_Extension_IP = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric1 SDA VN Extension IP. eg; 1.1.1.2$]"
#
# addVn()
# time.sleep(10)
# provisionVn()
# time.sleep(30)
# bgpConfig()
# time.sleep(5)
# provisionInt()