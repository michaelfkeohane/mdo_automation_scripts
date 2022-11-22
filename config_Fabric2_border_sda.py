'''
This will be called after the DNAC (SDA) Virtual Network (VN) has been setup

'''
import requests
import json
import os
import time
from requests.packages import urllib3
urllib3.disable_warnings()

def get_token():
    header_dictionary = {'Content-Type': 'application/json', 'Authorization': 'Basic YWRtaW46Q2lzY29WTVMxMDAl'}
    response = requests.post('https://10.85.189.34/dna/system/api/v1/auth/token', headers=header_dictionary, verify=False, timeout=60)
    json_dictionary_from_response = response.json()
    token = str(json_dictionary_from_response['Token'])
    return token

def addVn():
    headers = {'Content-Type': 'application/json', 'x-auth-token': get_token()}
    payload = [
        {
            "virtualNetworkName": Fabric2_VN,
            "siteNameHierarchy": Fabric2_SDA_Fabric_Name
        }
    ]
    request = requests.post('https://10.85.189.34/dna/intent/api/v1/business/sda/virtual-network', data=json.dumps(payload), headers=headers, verify=False, timeout=60)
    if request.status_code == 202:
        print ("Add VN to SDA: Passed")
    else:
        print ("Add VN to SDA: Failed")
    json_response = request.json()
    return (str(json_response))

def provisionVn():
    headers = {'Content-Type': 'application/json', 'x-auth-token': get_token()}
    payload = [
        {
            "virtualNetworkName": Fabric2_VN,
            "ipPoolName": Fabric2_IpPool_Name,
            "trafficType": "DATA",
            "authenticationPolicyName": "10_77_77_0-" + Fabric2_VN,
            "scalableGroupName": "",
            "isL2FloodingEnabled": False,
            "isThisCriticalPool": False,
            "poolType": "Generic"
        }
    ]
    request = requests.post('https://10.85.189.34/dna/intent/api/v1/business/sda/virtualnetwork/ippool', data=json.dumps(payload), headers=headers, verify=False, timeout=60)
    if request.status_code == 200:
        print ("Provision VN: Passed")
    else:
        print ("Provision VN: Failed")
    json_response = request.json()
    return (str(json_response))

def bgpConfig():
    headers = {'Content-Type': 'application/json', 'x-auth-token': get_token()}
    payload = {
        "forcePushTemplate": True,
        "isComposite": False,
        "mainTemplateId": "189ee26e-93ac-4e2d-b785-127e06de7282",
        "targetInfo": [
            {
                "hostName": "MSX-OTT02-ISR4431-08.cisco.com",
                "id": "1f3484e4-c600-4246-8366-e9472b7277f3",
                "params": {
                "VN_NAME": Fabric2_VN,
	    	"REMOTE_AS_NUMBER": "65502",
                "FUSION_VRF_IP_ADD": Fabric2_SDWAN_VN_Extension_IP,
                "VPN_NO": VPN_NO,
                "SDA_VN_Extension_IP": Fabric2_SDA_VN_Extension_IP,
	    	"AS_NUMBER": "65501"
	    	},
               "type": "MANAGED_DEVICE_UUID"
           }
       ],
       "templateId": "189ee26e-93ac-4e2d-b785-127e06de7282"
    }
    request = requests.post('https://10.85.189.34/dna/intent/api/v1/template-programmer/template/deploy', data=json.dumps(payload), headers=headers, verify=False, timeout=60)
    if request.status_code == 202:
        print ("BGP Configuration: Passed")
    else:
        print ("BGP Configuration: Failed")
    json_response = request.json()
    return (str(json_response))

def provisionInt():
    headers = {'Content-Type': 'application/json', 'x-auth-token': get_token()}
    payload = [
        {
            "siteNameHierarchy": "Global/MultiDomainSite/Fabric2",
            "deviceManagementIpAddress": "10.85.189.213",
            "interfaceName": "GigabitEthernet1/0/3",
            "dataIpAddressPoolName": "IntersiteReserve",
            "voiceIpAddressPoolName": "",
            "authenticateTemplateName": "No Authentication"
        }
    ]
    request = requests.post('https://10.85.189.34/dna/intent/api/v1/business/sda/hostonboarding/user-device', data=json.dumps(payload), headers=headers, verify=False, timeout=60)
    if request.status_code == 200:
        print ("Interface Provision: Passed")
    else:
        print ("Interface Provision: Failed")
    json_response = request.json()
    return (str(json_response))

Fabric2_VN = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric2 VN Name$]"
Fabric2_IpPool_Name = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric2 Reserved IP Pool Name$]"
Fabric2_SDA_Fabric_Name = "Global/MultiDomainSite/" + "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric2 - Fabric Name$]"
Fabric2_SDWAN_VN_Extension_IP = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric2 SDWAN VN Extension IP. eg; 2.1.1.1$]"
VPN_NO = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.SDWAN VPN ID$]"
Fabric2_SDA_VN_Extension_IP = "[$workflow.MultiDomain: SDA &lt;-&gt; SDWAN.input.Fabric2 SDA VN Extension IP. eg; 2.1.1.2$]"

addVn()
time.sleep(10)
provisionVn()
time.sleep(30)
bgpConfig()
time.sleep(5)
provisionInt()