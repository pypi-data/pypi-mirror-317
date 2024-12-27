import json
import os
import platform

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.constants import RESERVES
from colorama import Fore, init as init_colorama

init_colorama(autoreset=True)

# def option_check(alias):
#     if(alias=="default"):
#             return get_user_cred(alias)[0]
#     else:
#           return alias


class AliasServices:
    def __init__(self, alias):
        self.alias = alias

    def get_api_credentials(self):
        file= os.path.expanduser("~") + '/.E2E_CLI/config.json'
        file_reference = open(file, "r")
        config_file_object = json.loads(file_reference.read())
        if self.alias in config_file_object:
            if(self.alias=="default"):
                default_alias=config_file_object["default"]['api_key']
                return {"api_credentials": config_file_object[default_alias],
                        "message": "Valid alias"}
            else:
                return {"api_credentials": config_file_object[self.alias],
                        "message": "Valid alias"}
        else:
            return {"message": "Invalid alias provided"}

def system_file():
    if platform.system() == "Windows":  
                return f"{os.path.expanduser("~")}\\.E2E_CLI\\config.json"
    elif platform.system() == "Linux" or platform.system() == "Darwin":  
                return os.path.expanduser("~") + '/.E2E_CLI/config.json'


def get_user_cred(name, get_all=False):
    
    file= system_file()

    # try :
    # Opening JSON file
    f = open(file)

    has_keys = True if f.read() else False
    f.seek(0)
    # returns JSON object as a dictionary
    data = json.load(f) if has_keys else {}

    # view list of credentials incase of get_all==True
    if(name=="all" and get_all):
                try:
                    print("default --> ", data["default"]['api_key'])
                except:
                    print("default --> ", "Not set")
                return data.keys()
    f.close()

    if(name in data):
        if(name=="default"):
            return get_user_cred(data["default"]['api_key'])
        else:  
            return [ data[name]['api_auth_token'], data[name]['api_key'] ]
    else:
        print(f"{Fore.RED} ERROR : The given alias/credential doesn't exist")
        return None

def get_default_value(key):
    if not key:
        return None
    file= system_file()
    try:
        f = open(file)
    except FileNotFoundError:
        return None
    has_keys = True if f.read() else False
    f.seek(0)
    data = json.load(f) if has_keys else {}
    f.close()
    return data.get('default', {}).get(key, None)
