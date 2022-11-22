## API Working 11.18.22
def get_SDA_fabric_info():
    headers = {'Content-Type': 'application/json', "Accept": "application/json", 'x-auth-token': get_token()}
    payload = None

    # This is required ?siteNameHierarchy=1000
    # conn.request("GET", "/dna/intent/api/v1/business/sda/fabric?fabricName=<fabricName>")

    request = requests.get(f'{DNAC_URL}/dna/intent/api/v1/business/sda/fabric?fabricName=Fabric1', data=json.dumps(payload), headers=headers, verify=False, timeout=60)

    print(request.status_code)

    json_response = request.json()

    if request.status_code == API_SUCCESS:
        print(json_response["fabricDomainType"])
    else:
        print(f"get_SDA_fabric_info API: Non-Success API Code {request.status_code}")

    print(json_response)
    return (str(json_response))


# Function is failing claiming to need:
#{'status': 'failed', 'description': '
# Empty or Invalid virtualNetworkName in request body.
# Provide a valid virtualNetworkName and try again.',
# 'executionId': '3c3a56ab-9986-45d0-8970-6005206d6a10'}
def get_VN_Summary():
    headers = {'Content-Type': 'application/json', "Accept": "application/json",'x-auth-token': get_token()}
    payload = None
    siteNameHierarchy = "Global/US/Massachusetts/Boxboro-300/Floor-3"
    request = requests.get(f'{DNAC_URL}/dna/intent/api/v1/business/sda/virtual-network/summary?siteNameHierarchy={siteNameHierarchy}', data=json.dumps(payload), headers=headers, verify=False, timeout=60)

    print(request.status_code)
    print(request.json)

    if request.status_code == API_SUCCESS:
        print ("Passed")
    else:
        print ("Failed")

    json_response = request.json()
    print(json_response)

    return (str(json_response))

def get_VN():
    # conn.request("GET", "/dna/intent/api/v1/business/sda/virtual-network?virtualNetworkName "
    #                     "= < virtualNetworkName > & siteNameHierarchy = < siteNameHierarchy > ")
    headers = {'Content-Type': 'application/json', "Accept": "application/json",'x-auth-token': get_token()}
    payload = None
    siteNameHierarchy = "Global/US/Massachusetts/Boxboro-300/Floor-3"
    virtualNetworkName = "Fabric1_VN"
    request = requests.get(f'{DNAC_URL}/dna/intent/api/v1/business/sda/virtual-network?'
                           f'virtualNetworkName={virtualNetworkName}>&siteNameHierarchy={siteNameHierarchy}', data=json.dumps(payload), headers=headers, verify=False, timeout=60)

    print(request.status_code)
    print(request.json)

    if request.status_code == API_SUCCESS:
        print ("Passed")
    else:
        print ("Failed")

    json_response = request.json()
    print(json_response)

    return (str(json_response))
    pass
