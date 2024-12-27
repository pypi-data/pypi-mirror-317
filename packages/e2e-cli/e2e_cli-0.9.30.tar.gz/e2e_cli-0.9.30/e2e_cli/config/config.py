import json
import os
import platform

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.config.config_service import is_valid
from e2e_cli.core.constants import RESERVES
from colorama import Fore, init as init_colorama
from jsonschema import validate

init_colorama(autoreset=True)

class AuthConfig:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.home_directory = os.path.expanduser("~")
        if platform.system() == "Windows":
            self.folder = f"{self.home_directory}\\.E2E_CLI"
            self.file = f"{self.home_directory}\\.E2E_CLI\\config.json"
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            self.folder = f"{self.home_directory}/.E2E_CLI"
            self.file = f"{self.home_directory}/.E2E_CLI/config.json"


    def windows_hider(self):
        os.system("attrib +h " + self.folder)

    def windows_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        elif not os.path.isfile(self.file):
            self.windows_hider()
            return 0
        else:
            self.windows_hider()
            return 1

    def linux_mac_file_check(self):
        if not os.path.isdir(self.folder):
            return -1
        elif not os.path.isfile(self.file):
            return 0
        else:
            return 1
        
    def check_if_file_exist(self):
        if platform.system() == "Windows":
            return self.windows_file_check()
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            return self.linux_mac_file_check()

    def reserve_keyword_check(self):
        if(str(self.kwargs["alias"]).lower() in RESERVES):
                print("The used alias name is a reserve keyword for cli tool")            
        else:
                self.add_json_to_file()

    def check_file_formate(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except Exception as e:
            # logger.error(f"ERROR | CONFIG | check_file_formate | Error while open user's config file : {str(e)}")
            return False
        
        try:
            schema = {
                "$schema": "http://json-schema.org/draft-04/schema#",
                "type": "object",
                "properties": {
                    "api_key": {
                    "type": "string"
                    },
                    "api_auth_token": {
                    "type": "string"
                    }
                },
                "required": [
                    "api_key",
                    "api_auth_token"
                ]
            }
            for key in data.keys():
                validate(instance=data[key], schema=schema)
            return True
        except Exception as e:
            return False

    def copy_file_content(self, path):
        try:
            with open(path, 'r') as src:
                with open(self.file, 'w') as dest:
                    for line in src:
                        dest.write(line)
            return True
        except Exception as e:
            return False

    def add_json_to_file(self):
        api_access_credentials_object = {"api_key": self.kwargs["api_key"],
                                         "api_auth_token": self.kwargs["api_auth_token"]}
        if(is_valid(api_access_credentials_object["api_key"], api_access_credentials_object["api_auth_token"])):
            with open(self.file, 'r+') as file_reference:
                read_string = file_reference.read()
                if read_string == "":
                    file_reference.write(json.dumps({self.kwargs["alias"]:
                                                        api_access_credentials_object}))
                else:
                    api_access_credentials = json.loads(read_string)
                    api_access_credentials.update({self.kwargs["alias"]:
                                                    api_access_credentials_object})
                    file_reference.seek(0)
                    file_reference.write(json.dumps(api_access_credentials))
            
            print("Alias/user_name/Token name successfully added")
        else:
            
            print("Invalid credentials given please enter correct Api key and Authorisation")
            return


    def add_to_config(self):
        file_exist_check_variable = self.check_if_file_exist()
        if file_exist_check_variable == -1:
            os.mkdir(self.folder)
            with open(self.file, 'w'):
                pass
            self.reserve_keyword_check()
        elif file_exist_check_variable == 0:
            with open(self.file, 'w'):
                pass
            self.reserve_keyword_check()
        elif file_exist_check_variable == 1:
            if (get_user_cred(self.kwargs['alias'],2)):
                print("The given alias/username already exist!! Please use another name or delete the previous one")
            else:
                self.reserve_keyword_check()


    def delete_from_config(self, x=0):
        file_exist_check_variable = self.check_if_file_exist()
        if file_exist_check_variable == -1 or file_exist_check_variable == 0:
            print(f"{Fore.RED}You need to add your api access credentials using the add functionality ")
            print("To know more please write 'e2e_cli alias -h' on your terminal")

        elif file_exist_check_variable == 1:
            with open(self.file, 'r+') as file_reference:
                file_contents_object = json.loads(file_reference.read())
                delete_output = file_contents_object.pop(self.kwargs["alias"], 'No key found')

                if delete_output == "No key found" and x!=1:
                    print(f"{Fore.RED}No such alias found. Please re-check and enter again")
                else:
                    file_reference.seek(0)
                    file_reference.write(json.dumps(file_contents_object))
                    file_reference.truncate()
                    if(x!=1):
                        print("Alias/name Successfully deleted")


    def adding_config_file(self, path):
        # for drag and drop
        if(path[0]=="'" and path[-1]=="'"):
                    path=path.lstrip(path[0])
                    path=path.rstrip(path[-1])

        if(path.endswith(".json") and os.path.isfile(path)):
            if(not self.check_file_formate(path)):
                print(f"{Fore.RED} Error: config file format is wrong!!")
                return
            if(self.check_if_file_exist()==-1):
                os.mkdir(self.folder)  
            if(not self.copy_file_content(path)):
                print(f"{Fore.RED} Error: read and write error in local file system.")
                return
            print("Token file successfuly added")


    def set_default(self):
        api_access_credentials_object = {"api_key": self.kwargs["api_key"],
                                         "api_auth_token": self.kwargs["api_auth_token"],
                                         "project_id": self.kwargs["project_id"],
                                         "location": self.kwargs["location"]}
        with open(self.file, 'r+') as file_reference:
                read_string = file_reference.read()
                if read_string == "":
                    file_reference.write(json.dumps({"default":
                                                        api_access_credentials_object}))
                else:
                    api_access_credentials = json.loads(read_string)
                    api_access_credentials.update({"default":
                                                    api_access_credentials_object})
                    file_reference.seek(0)
                    file_reference.truncate(0)                    
                    file_reference.write(json.dumps(api_access_credentials))
