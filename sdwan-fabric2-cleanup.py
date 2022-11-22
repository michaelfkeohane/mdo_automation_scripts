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
VPN_FT_NAME = ('IntersiteVN_VPN_Template4451')
VPN_INT_FT_NAME = ('IntersiteVN_VPN_Interface_Template4451')
BGP_FT_NAME = ('IntersiteVN_BGP_VPN_Template4451')
ft_list = [VPN_FT_NAME, VPN_INT_FT_NAME, BGP_FT_NAME]

print ("Downloading Templates")
urllib.request.urlretrieve ("http://10.85.189.49/demo/4451_attach.json", "4451_attach.json")
urllib.request.urlretrieve ("http://10.85.189.49/demo/4451_input.json", "4451_input.json")
urllib.request.urlretrieve ("http://10.85.189.49/demo/4451_default_dt.json", "4451_default_dt.json")

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

def default_dt(device, device_id):
    cookies = get_token("https://10.85.189.187", "poc-cred", "poc-cred")
    headers = {'Content-Type': 'application/json', 'Accept' : 'application/json', 'x-xsrf-token': cookies[1]}
    print ('---------- Updating DT ----------')
    request1 = requests.put("https://10.85.189.187/dataservice/template/device/" + device, data=open(device_id + '_default_dt.json', 'rb'), headers=headers, cookies=cookies[0], verify=False, timeout=60)
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
    return request3.text

def delete_ft():
    cookies = get_token("https://10.85.189.187", "poc-cred", "poc-cred")
    headers = {'Content-Type': 'application/json', 'Accept' : 'application/json'}
    request = requests.get("https://10.85.189.187:443/dataservice/template/feature?summary=true", headers=headers, cookies=cookies[0], verify=False, timeout=60)
    json_response = request.json()
    for ft in ft_list:
        counter = 0
        while counter < 500:
            templateName = str(json_response['data'][counter]['templateName'])
            templateId = str(json_response['data'][counter]['templateId'])
            if templateName == ft:
                print (ft, "is Object", counter)
                print (ft, "id =", templateId)
                break
            else:
                print ("Object", counter, "is not", ft)
            counter+=1
        response = requests.delete("https://10.85.189.187:443/dataservice/template/feature/" + templateId, headers=headers, cookies=cookies[0], verify=False, timeout=60)
        if response.status_code == 200:
            print (ft, 'Delete: Successful')
        else:
            print (ft, 'Delete: Failed')
    return response.status_code


print ('Cleaning ISR4451')
default_dt(isr4451, "4451")
time.sleep(50)
delete_ft()
