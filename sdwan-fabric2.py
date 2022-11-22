#!/usr/bin/python

import requests
import json
import os
import time
import sys
import urllib.request
from requests.packages import urllib3
urllib3.disable_warnings()

VPN_NO = "500"
VPN_TEMPLATE_NAME = ('IntersiteVN_VPN_Template')
VPN_INT_TEMPLATE_NAME = ('IntersiteVN_VPN_Interface_Template')
BGP_TEMPLATE_NAME = ('IntersiteVN_BGP_VPN_Template')
BGP_LOCAL_IP = (sys.argv[1] + '/24')
BGP_NEIGHBOR_IP = sys.argv[2]

print ("Downloading Templates")
urllib.request.urlretrieve ("http://10.85.189.49/demo/4321_attach.json", "4321_attach.json")
urllib.request.urlretrieve ("http://10.85.189.49/demo/4321_input.json", "4321_input.json")
urllib.request.urlretrieve ("http://10.85.189.49/demo/4451_attach.json", "4451_attach.json")
urllib.request.urlretrieve ("http://10.85.189.49/demo/4451_input.json", "4451_input.json")
urllib.request.urlretrieve ("http://10.85.189.49/demo/bgp_ft_payload.json", "bgp_ft_payload.json")
urllib.request.urlretrieve ("http://10.85.189.49/demo/vpn_ft_payload.json", "vpn_ft_payload.json")
urllib.request.urlretrieve ("http://10.85.189.49/demo/vpn_int_ft_payload.json", "vpn_int_ft_payload.json")

isr4321 = "936bfcdf-5fa7-477c-ba9b-bd5ec3ad566d"
isr4451 = "276e95af-23bc-4b52-a6c8-15df3c20bcaa"

def get_token(url, username, password):
    login_data = {'j_username': username, 'j_password': password}
    header_dictionary = {'Content-Type': 'application/x-www-form-urlencoded'}
    endpoint = "/j_security_check"
    request = requests.post(url + endpoint, data=login_data, headers=header_dictionary, verify=False, timeout=60)
    cookies = {'JSESSIONID': (request.cookies['JSESSIONID'])}
    request2 = requests.get('https://10.85.189.187/dataservice/client/token', headers=header_dictionary, cookies=cookies, verify=False, timeout=60)
    token = (request2.text)
    return (cookies, token)

def replacement(where, old_text, new_text):
    rep = where.find(old_text)
    return where[:rep + len(old_text)] + new_text + where[rep + len(old_text):]

def vpn_ft(device):
    cookies = get_token("https://10.85.189.187", "poc-cred", "poc-cred")
    headers = {'Content-Type': 'application/json', 'Accept' : 'application/json'}
    try:
        os.remove('vpn_ft.json')
    except OSError:
        print('File vpn_ft.json does not exist... Creating it')
        pass
    payloadIn = open("vpn_ft_payload.json", "rt")
    payloadOut = open("vpn_ft.json", "wt")
    for line in payloadIn:
        payloadOut.write(line.replace('VPN_TEMPLATE_NAME', VPN_TEMPLATE_NAME + device).replace('VPN_NO', VPN_NO))
    payloadIn.close()
    payloadOut.close()
    request = requests.post("https://10.85.189.187:443/dataservice/template/feature", data=open('vpn_ft.json', 'rb'), headers=headers, cookies=cookies[0], verify=False, timeout=60)
    json_response = request.json()
    return str(json_response['templateId'])

def vpn_int_ft(device):
    cookies = get_token("https://10.85.189.187", "poc-cred", "poc-cred")
    headers = {'Content-Type': 'application/json', 'Accept' : 'application/json'}
    try:
        os.remove('vpn_int_ft.json')
    except OSError:
        print('File vpn_int_ft.json does not exist... Creating it')
        pass
    payloadIn = open("vpn_int_ft_payload.json", "rt")
    payloadOut = open("vpn_int_ft.json", "wt")
    for line in payloadIn:
        payloadOut.write(line.replace('VPN_INT_TEMPLATE_NAME', VPN_INT_TEMPLATE_NAME + device).replace('VPN_NO', VPN_NO).replace('BGP_LOCAL_IP', BGP_LOCAL_IP))
    payloadIn.close()
    payloadOut.close()
    request = requests.post("https://10.85.189.187:443/dataservice/template/feature", data=open('vpn_int_ft.json', 'rb'), headers=headers, cookies=cookies[0], verify=False, timeout=60)
    json_response = request.json()
    return str(json_response['templateId'])

def bgp_ft(device):
    cookies = get_token("https://10.85.189.187", "poc-cred", "poc-cred")
    headers = {'Content-Type': 'application/json', 'Accept' : 'application/json'}
    try:
        os.remove('bgp_ft.json')
    except OSError:
        print('File bgp_ft.json does not exist... Creating it')
        pass
    payloadIn = open("bgp_ft_payload.json", "rt")
    payloadOut = open("bgp_ft.json", "wt")
    for line in payloadIn:
        payloadOut.write(line.replace('BGP_TEMPLATE_NAME', BGP_TEMPLATE_NAME + device).replace('BGP_NEIGHBOR_IP', BGP_NEIGHBOR_IP).replace('VPN_NO', VPN_NO))
    payloadIn.close()
    payloadOut.close()
    request = requests.post("https://10.85.189.187:443/dataservice/template/feature", data=open('bgp_ft.json', 'rb'), headers=headers, cookies=cookies[0], verify=False, timeout=60)
    json_response = request.json()
    return str(json_response['templateId'])

def create_dt(device, device_id):
    cookies = get_token("https://10.85.189.187", "poc-cred", "poc-cred")
    headers = {'Content-Type': 'application/json', 'Accept' : 'application/json', 'x-xsrf-token': cookies[1]}
    try:
        os.remove('template.json')
    except OSError:
        print('File template.json does not exist... Creating it')
        pass
    try:
        os.remove('dt.json')
    except OSError:
        print('File dt.json does not exist... Creating it')
        pass
    print ('---------- GET latest DT ----------')
    request = requests.get("https://10.85.189.187/dataservice/template/device/object/" + device, cookies=cookies[0], verify=False, timeout=60)
    if request.status_code == 200:
        print (device_id, 'GET latest DT: Successful')
    else:
        print (device_id, 'GET latest DT: Failed')
    file = open("template.json", "w")
    file.write(request.text)
    file.close()
    print ('Updating DT with new VPN Configurations')
    with open("template.json") as temp:
        perm = open("dt.json", 'a+')
        for line in temp.readlines():
            build = replacement(line, "\"generalTemplates\":[", "{\"templateId\": \"" + vpn_ft(device_id) + "\",\"templateType\": \"vpn-vedge\",\"subTemplates\": [{\"templateId\": \"" + vpn_int_ft(device_id) + "\",\"templateType\": \"vpn-vedge-interface\"},{\"templateId\": \"" + bgp_ft(device_id) + "\",\"templateType\": \"bgp\"}]},")
            perm.write(build)
        perm.close()
        temp.close()
    print ('---------- Updating DT ----------')
    request1 = requests.put("https://10.85.189.187/dataservice/template/device/" + device, data=open('dt.json', 'rb'), headers=headers, cookies=cookies[0], verify=False, timeout=60)
    if request1.status_code == 200:
        print (device_id, 'DT Update: Successful')
    else:
        print (device_id, 'DT Update: Failed')

    print ('---------- Editing DT ----------')
    request2 = requests.post("https://10.85.189.187/dataservice/template/device/config/input/", data=open(device_id +'_input.json', 'rb'), headers=headers, cookies=cookies[0], verify=False, timeout=60)
    if request2.status_code == 200:
        print (device_id, 'Edit DT: Successful')
    else:
        print (device_id, 'Edit DT: Failed')

    print ('---------- Attaching DT ----------')
    request3 = requests.post("https://10.85.189.187/dataservice/template/device/config/attachfeature", data=open(device_id +'_attach.json', 'rb'), headers=headers, cookies=cookies[0], verify=False, timeout=60)
    if request3.status_code == 200:
        print (device_id, 'Attach DT: Successful')
    else:
        print (device_id, 'Attach DT: Failed')
    return request3.text


print ('Configuring ISR4451')
create_dt(isr4451, "4451")
