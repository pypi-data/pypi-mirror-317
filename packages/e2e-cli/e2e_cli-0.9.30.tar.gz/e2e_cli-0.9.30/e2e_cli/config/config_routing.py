import subprocess
import re
from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core import show_messages
from e2e_cli.config.config import AuthConfig
from e2e_cli.core.alias_service import get_user_cred, get_default_value
from e2e_cli.core.constants import LOCATION_OPTION
from colorama import Fore, init as init_colorama

init_colorama(autoreset=True)

class ConfigRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, Parsing_errors):

        if self.arguments.args.alias_commands == 'add':
            try:
                api_key = input("Enter your api key: ")
                auth_token = input("Enter your auth token: ")
                auth_config_object = AuthConfig(alias=input("Input name of alias you want to add : "),
                                                    api_key=api_key,
                                                    api_auth_token=auth_token)
                auth_config_object.add_to_config()
            except KeyboardInterrupt:
                print(" ")
                pass

        elif self.arguments.args.alias_commands == 'add_file':
                path=input("input the file path : ")
                auth_config_object = AuthConfig()
                auth_config_object.adding_config_file(path)
                return

        elif self.arguments.args.alias_commands == 'delete':  
            delete_alias=input("Input name of alias you want to delete : ")
            if delete_alias == get_default_value("api_key"):
                print(f"{Fore.RED}You can't delete default alias")
                return
            confirmation =input("are you sure you want to delete press y for yes, else any other key : ")
            if(confirmation.lower()=='y'):
                auth_config_object = AuthConfig(alias=delete_alias)
                try:
                    auth_config_object.delete_from_config()
                except:
                    pass  

        elif self.arguments.args.alias_commands == 'view':
            file_exist_check_variable = AuthConfig().check_if_file_exist()
            if file_exist_check_variable == -1 or file_exist_check_variable == 0:
                print(f"{Fore.RED}You need to add your api access credentials using the add functionality ")
                subprocess.call(['e2e_cli', "alias","-h"])
                return

            for item in list(get_user_cred("all", get_all=True)):
                if(type(item)==str and not item.startswith("default")):
                    print(item)
            default_project_id, default_location = get_default_value("project_id"), get_default_value("location")
            print("=========================")
            print("default location : ", default_location)
            print("default project_id : ", default_project_id)

        elif self.arguments.args.alias_commands == 'set':
            try:
                default_alias=input("Enter name of the alias you want to set as default : ")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Exit with error code 1")
                pass
            if not get_user_cred(default_alias):
                show_messages.show_parsing_error(Parsing_errors)
                return

            try:
                default_project_id = input("Enter project_id you want to set as default : ")
                if not re.match(r"^[1-9]\d*$", default_project_id):
                    print(f"{Fore.RED} project_id must be a positive integer")
                    return
                default_location = input("Enter location you want to set as default (Delhi/Mumbai): ")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Exit with error code 1")
                return
            if default_location not in LOCATION_OPTION:
                print(f"{Fore.RED} Error: Default location not set. Enter correct location.")
                show_messages.show_parsing_error(Parsing_errors)
                return

            if(input("are you sure you want to proceed (y/n): ").lower()=="y"):
                try:
                    AuthConfig(alias="default").delete_from_config(x=1)
                    auth_config_object = AuthConfig(alias="default",
                                                    api_key=default_alias,
                                                    api_auth_token=default_alias,
                                                    project_id=default_project_id,
                                                    location=default_location,
                                                    )
                    auth_config_object.set_default()
                    print(f"{Fore.GREEN}Default alias set to : {default_alias}")
                    print(f"{Fore.GREEN}Default location set to : {default_location}")
                    print(f"{Fore.GREEN}Default project id set to : {default_project_id}")
                except KeyboardInterrupt:
                    print(f"{Fore.RED}Operation revoked. unable to set default alias, location, project_id")
                    pass
                except Exception as e:
                    print(f"{Fore.RED}Error: {str(e)}")
                    show_messages.show_parsing_error(Parsing_errors)
            else:
                print(f"{Fore.RED}Operation revoked. unable to set default alias, location, project_id")
                show_messages.show_parsing_error(Parsing_errors)
        else:
            print("Command not found!!")
            show_messages.show_parsing_error(Parsing_errors)