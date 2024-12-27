import os
import re

from colorama import Fore
from colorama import init as init_colorama

from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.apiclient import ApiClient
from e2e_cli.core.helper_service import Checks
from e2e_cli.faas.constants import (DEFAULT_FUNCTION_CONFIG,
                                    DEFAULT_FUNCTION_CONFIG_NAME,
                                    LANGUAGE_OPTIONS, NAME_VALIDATION_MESSAGE,
                                    RUNTIME_API_ENDPOINT,
                                    RUNTIME_LANGUAGE_MAPPING,
                                    SOURCE_CODE_FILE_NAME, VALIDATE_NAME_REGEX)
from e2e_cli.faas.helper_service import HelperService

init_colorama(autoreset=True)

class SetupService:
    def __init__(self, **kwargs):
        self.user_creds = get_user_cred(kwargs.get("alias"))
        self.api_key = self.user_creds[1]
        self.auth_token = self.user_creds[0]
        self.arguments = kwargs.get("arguments")
        self.project_id = self.arguments.args.project_id
        self.location = self.arguments.args.location
    
    def caller(self, method):
        allowed_method = {
            "init": self.setup
        }
        return allowed_method.get(method)
        
    def format_runtimes(self, response):
        runtimes = response.get("data")
        language_templates = dict()
        for runtime_detail in runtimes:
            language = RUNTIME_LANGUAGE_MAPPING.get(runtime_detail.get("runtime"))
            if language:
                language_templates.update({language : runtime_detail})
        return language_templates

    def get_runtimes(self):
        response = ApiClient(self.api_key, self.auth_token, self.project_id, self.location).get_response(RUNTIME_API_ENDPOINT, "GET")
        if not response:
            return None
        if response.get("code") != 200:
            Checks.status_result(response)
        return self.format_runtimes(response)
        
    def setup(self):
        language = self.arguments.args.lang
        function_name = self.arguments.args.name
        timeout = self.arguments.args.timeout
        memory = self.arguments.args.memory
        compute_type = self.arguments.args.compute_type
        available_runtime = self.get_runtimes()
        if not available_runtime or not available_runtime.get(language):
            print(f"{Fore.RED}Error: The language name you entered is either invalid or not supported by E2E-Function.")
            return
        setup_details = available_runtime.get(language)
        valid_pattern = re.compile(VALIDATE_NAME_REGEX)

        if not re.fullmatch(valid_pattern, function_name):
            print(f"{Fore.RED}Please enter the valid function name. {NAME_VALIDATION_MESSAGE}")
            return
        if setup_details.get("node_type") != compute_type:
            print(f"{Fore.RED}Error: The compute type you entered/default ({compute_type}) does not allowed for the given runtime ({language}).")
            return
        current_working_directory = os.getcwd()
        try:
            os.mkdir(f"{current_working_directory}/{function_name}")
        except Exception as e:
            print(f"{Fore.RED}{e}")
            return
        
        if os.path.exists(f"{current_working_directory}/{function_name}"):
            os.chdir(f"{current_working_directory}/{function_name}")
            HelperService.create_file_with_template_code(f"{SOURCE_CODE_FILE_NAME.get(language)}", setup_details.get("boiler_code"))
            HelperService.create_file_with_template_code(setup_details.get("label"), setup_details.get("requirements_code"))
            DEFAULT_FUNCTION_CONFIG["function"]["name"] = function_name
            DEFAULT_FUNCTION_CONFIG["function"]["runtime"] = language
            DEFAULT_FUNCTION_CONFIG["function"]["limits"]["memory"] = memory
            DEFAULT_FUNCTION_CONFIG["function"]["limits"]["timeout"] = timeout
            DEFAULT_FUNCTION_CONFIG["function"]["compute_type"] = compute_type
            HelperService.create_yaml_file_with_template_code(DEFAULT_FUNCTION_CONFIG_NAME, DEFAULT_FUNCTION_CONFIG)
        else:
            print(f"{Fore.RED}Error -- Can not able to locate the setup directory.")
            return
        print(f"{Fore.GREEN}Setup is successfully completed. kindly check folder {function_name} in current directory.")

        