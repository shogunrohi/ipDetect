import os.path
def run():
    if os.path.exists("token.txt"):
        file = open("token.txt", "r")
        api_key = file.read()
        file.close()
        api_access = "https://vpnapi.io/api/~?key="
        return api_key, api_access
    else:
        api_key =  ""
        api_access = "https://vpnapi.io/api/~?key="
        return api_key, api_access

def reset(api):
    api_access2 = "https://vpnapi.io/api/~?key="
    api_key2 = api[api.index("=")+ 1:]
    return api_access2 + api_key2

def savekey(tken):
    file = open("token.txt","w")
    file.write(tken)
    file.close()

