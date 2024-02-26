def run():
    api_key =  ""
    api_access =  "https://vpnapi.io/api/-?key="
    return api_key, api_access

def reset(api):
    api_access2 = "https://vpnapi.io/api/~?key="
    api_key2 = api[api.index("=")+ 1:]
    return api_access2 + api_key2
